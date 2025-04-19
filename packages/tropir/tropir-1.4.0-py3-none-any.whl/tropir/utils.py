from datetime import datetime
import json
from pathlib import Path
import traceback
import functools
import time
import os
import uuid

from loguru import logger

from .config import DEFAULT_API_URL
from .constants import (
    _thread_local, 
    _process_default_session_id
)
# Helper functions for managing LLM tracking sessions and thread-local storage
def manage_session_id(session_id):
    """Manage thread-local session ID for LLM calls"""
    previous_session_id = getattr(_thread_local, 'session_id', None)
    if session_id:
        _thread_local.session_id = session_id
        logger.debug(f"Using provided session ID for LLM call: {session_id}")
    return previous_session_id

def restore_session_id(previous_session_id):
    """Restore previous session ID after an LLM call"""
    if previous_session_id:
        _thread_local.session_id = previous_session_id
        logger.debug(f"Restored previous session ID: {previous_session_id}")

def create_base_log_entry(provider, request_args):
    """
    Create a base log entry with standardized structure for all providers.
    
    Args:
        provider (str): The LLM provider name (openai, anthropic, bedrock)
        request_args (dict): The provider-specific request arguments
        
    Returns:
        dict: A standardized log entry object with base fields
    """
    # Generate a unique log ID
    log_id = str(uuid.uuid4())
    
    # Get or create session ID
    if hasattr(_thread_local, 'session_id') and _thread_local.session_id:
        session_id = _thread_local.session_id
    else:
        session_id = _process_default_session_id
    
    # Create ISO 8601 timestamp
    timestamp = datetime.utcnow().isoformat()
    
    # Extract and standardize request fields
    standard_request = {
        # Core required fields
        "model": request_args.get("model") or request_args.get("modelId", "unknown"),
        "messages": request_args.get("messages", []),
        
        # Standard parameters (all providers)
        "temperature": request_args.get("temperature"),
        "max_tokens": request_args.get("max_tokens") or request_args.get("maxTokens"),
        "top_p": request_args.get("top_p") or request_args.get("topP"),
        
        # OpenAI-specific parameters (may be null for other providers)
        "frequency_penalty": request_args.get("frequency_penalty"),
        "presence_penalty": request_args.get("presence_penalty"),
        "stop": request_args.get("stop"),
        "n": request_args.get("n"),
    }
    
    # Add tools if present
    if "tools" in request_args:
        standard_request["tools"] = request_args.get("tools")
    
    # Add tool_choice if present
    if "tool_choice" in request_args:
        standard_request["tool_choice"] = request_args.get("tool_choice")
    
    # Create base log entry
    log_entry = {
        "log_id": log_id,
        "session_id": session_id,
        "timestamp": timestamp,
        "provider": provider,
        "request": standard_request,
        
        # Empty fields to be filled in by specific provider logging functions
        "response": "",
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "token_details": {
                "cached_tokens": None,
                "audio_tokens": None,
                "reasoning_tokens": None,
                "accepted_prediction_tokens": None,
                "rejected_prediction_tokens": None
            }
        },
        "duration": 0,
        "success": False,
    }
    
    return log_entry

def create_generic_method_wrapper(original_method, provider, log_function):
    """Create a generic wrapper for LLM API methods"""
    @functools.wraps(original_method)
    def wrapped_method(*args, **kwargs):

        # Extract session_id if provided directly in kwargs
        session_id = kwargs.pop('session_id', None)
        previous_session_id = manage_session_id(session_id)
        
        start_time = time.perf_counter()
        success = True
        response_data = None
        
        try:
            response_data = original_method(*args, **kwargs)
            return response_data
        except Exception as e:
            success = False
            response_data = {"error": str(e), "traceback": traceback.format_exc()}
            logger.error(f"LLM call to {provider} failed: {e}")
            raise
        finally:
            duration = time.perf_counter() - start_time
            try:
                # Debug logging
                logger.debug(f"Calling log function for {provider} with success={success}") 
                # Call the provider-specific log function
                log_function(provider, kwargs, response_data, duration, success)
            except Exception as e:
                logger.error(f"Error during LLM tracking for {provider}: {e}")
                logger.error(traceback.format_exc())
            
            restore_session_id(previous_session_id)
    
    # Mark the patched function so we don't patch it again
    wrapped_method._llm_tracker_patched = True
    return wrapped_method

def create_async_method_wrapper(original_async_method, provider, log_function):
    """Create a generic async wrapper for LLM API methods"""
    @functools.wraps(original_async_method)
    async def async_wrapped_method(*args, **kwargs):
        # Extract session_id if provided directly in kwargs
        session_id = kwargs.pop('session_id', None)
        previous_session_id = manage_session_id(session_id)
        
        start_time = time.perf_counter()
        success = True
        response_data = None
        
        try:
            response_data = await original_async_method(*args, **kwargs)
            return response_data
        except Exception as e:
            success = False
            response_data = {"error": str(e), "traceback": traceback.format_exc()}
            logger.error(f"Async LLM call to {provider} failed: {e}")
            raise
        finally:
            duration = time.perf_counter() - start_time
            try:
                # Call the provider-specific log function
                log_function(provider, kwargs, response_data, duration, success)
            except Exception as e:
                logger.error(f"Error during LLM tracking for {provider}: {e}")
                logger.error(traceback.format_exc())
            
            restore_session_id(previous_session_id)
    
    # Mark the patched function so we don't patch it again
    async_wrapped_method._llm_tracker_patched = True
    return async_wrapped_method

def get_user_id():
    """
    Validates the API key from environment variables and returns the user_id.
    
    Returns:
        str: User ID if validation successful, None otherwise
    """
    import os
    import requests
    
    # Load TROPIR environment variables if they haven't been loaded already
    try:
        import re
        from pathlib import Path
        
        env_path = Path('.env')
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Look for TROPIR_API_KEY and TROPIR_API_URL specifically
                        if match := re.match(r'^(TROPIR_API_KEY|TROPIR_API_URL)\s*=\s*(.*)$', line):
                            key = match.group(1)
                            value = match.group(2).strip()
                            # Remove quotes if present
                            if (value[0] == value[-1] == '"' or value[0] == value[-1] == "'"):
                                value = value[1:-1]
                            os.environ[key] = value
    except Exception:
        pass
    
    # Get API key from environment variables
    api_key = os.environ.get("TROPIR_API_KEY")
    
    if not api_key:
        logger.error("TROPIR_API_KEY environment variable not set")
        return None
    
    try:
        # Use either environment variable for base URL or default
        base_url = os.environ.get("TROPIR_API_URL", DEFAULT_API_URL)
        endpoint = f"{base_url}api/api-key"
        
        logger.debug(f"Making API request to: {endpoint}")
        
        # Make the API request synchronously
        response = requests.post(
            endpoint,
            json={"api_key": api_key},
            timeout=10.0
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Check for empty response
        if not response.text:
            logger.error("Empty response received from API")
            return None
            
        # Try to parse the response
        try:
            result = response.json()
            
            if result.get("status") == "ok" and "user_id" in result:
                user_id = result.get("user_id")
                return user_id
            else:
                error_msg = result.get("message", "Unknown error")
                logger.error(f"API key validation failed: {error_msg}")
                return None
                
        except ValueError as json_err:
            # Log the response content for debugging
            logger.error(f"Failed to parse JSON response: {json_err}")
            logger.debug(f"Response status code: {response.status_code}")
            logger.debug(f"Response content: {response.text[:500]}")  # Log first 500 chars
            return None
        
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request failed: {req_err}")
        return None
    except Exception as e:
        logger.error(f"Error validating API key: {str(e)}")
        return None