"""
Amazon Bedrock-specific patching logic for LLM tracking.
"""

import functools
import time
import traceback
import json
import os
import uuid
from datetime import datetime
from loguru import logger
from pathlib import Path
import logging

from .constants import (
    TOKEN_COUNT_KEYS,
    DEFAULT_TOKEN_COUNT
)
from .utils import (
    create_base_log_entry,
)
from tropir.transport import send_log

logger = logging.getLogger(__name__)

# Define model prefixes/identifiers for different providers in Bedrock
BEDROCK_MODEL_PREFIXES = {
    "anthropic": ["anthropic.", "claude-"],
    "ai21": ["ai21."],
    "amazon": ["amazon.titan-"],
    "cohere": ["cohere."],
    "meta": ["meta.llama"],
    "mistral": ["mistral."]
}

def process_bedrock_messages(body):
    """Process Bedrock request body to extract messages and other fields."""
    try:
        # If body is a string, try to parse it as JSON
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                return {}
        
        # If body is not a dict, return empty dict
        if not isinstance(body, dict):
            return {}
        
        # Extract messages if present
        messages = []
        if "messages" in body:
            for msg in body["messages"]:
                if isinstance(msg, dict):
                    # Handle content that might be in different formats
                    content = msg.get("content", "")
                    
                    # If content is a list (array of objects with text fields)
                    if isinstance(content, list):
                        # Combine all text fields into a single string
                        combined_text = ""
                        for item in content:
                            if isinstance(item, dict) and "text" in item:
                                combined_text += item["text"] + "\n"
                        content = combined_text.strip()
                    
                    # Create standardized message format
                    standardized_msg = {
                        "role": msg.get("role", "user"),
                        "content": content
                    }
                    messages.append(standardized_msg)
        
        # Create processed body with standardized messages
        processed_body = {}
        if messages:
            processed_body["messages"] = messages
        
        # Copy other relevant fields
        for field in ["system", "tools", "tool_choice", "max_tokens", "temperature", "top_p"]:
            if field in body:
                processed_body[field] = body[field]
        
        return processed_body
    
    except Exception as e:
        logger.error(f"Error processing Bedrock messages: {str(e)}")
        return {}

def redact_base64_data(data):
    """Recursively redact base64 data from nested structures"""
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            # Check if the key might contain image data
            if any(img_key in key.lower() for img_key in ["image", "photo", "picture", "media"]):
                if isinstance(value, str) and len(value) > 100 and "," in value:
                    # Likely a base64 string, redact it
                    result[key] = "[BASE64_DATA_REMOVED]"
                else:
                    result[key] = redact_base64_data(value)
            else:
                result[key] = redact_base64_data(value)
        return result
    elif isinstance(data, list):
        return [redact_base64_data(item) for item in data]
    else:
        # Check if this might be a base64 string (simple heuristic)
        if isinstance(data, str) and len(data) > 500 and "base64" in data.lower():
            return "[BASE64_DATA_REMOVED]"
        return data

def extract_bedrock_response_content(response, model_id):
    """Extract the content from a Bedrock response based on the model type"""
    if not response:
        return "", {}, None
    
    response_text = ""
    usage = {}
    function_call_info = None
    
    try:
        # Newer Bedrock Claude format (direct output field with message and content)
        if isinstance(response, dict) and "output" in response:
            output = response["output"]
            if isinstance(output, dict) and "message" in output:
                message = output["message"]
                if isinstance(message, dict) and "content" in message:
                    content = message["content"]
                    
                    # Handle list-type content (common in Claude responses)
                    if isinstance(content, list):
                        has_tool_use = False
                        for item in content:
                            if isinstance(item, dict):
                                # Handle text content
                                if "text" in item:
                                    response_text += item["text"]
                                
                                # Handle tool use content - structured like the example in user query
                                if "toolUse" in item:
                                    has_tool_use = True
                                    tool_use = item["toolUse"]
                                    tool_name = tool_use.get("name", "unknown")
                                    tool_input = tool_use.get("input", {})
                                    tool_id = tool_use.get("toolUseId", "tooluse_default")
                                    
                                    # Create function call info structure identical to Anthropic format
                                    function_call_info = {
                                        "type": "tool_calls",
                                        "calls": [
                                            {
                                                "id": tool_id,
                                                "type": "function",
                                                "function": {
                                                    "name": tool_name,
                                                    "arguments": json.dumps(tool_input)
                                                }
                                            }
                                        ]
                                    }
                        
                        # If we detected a tool use, note this in the response text
                        if has_tool_use and function_call_info:
                            # We don't need to add tool use to response text as it's now in function_call_info
                            pass
                    
                    # Handle string content
                    elif isinstance(content, str):
                        response_text = content
        
        # Extract usage information if available
        if "usage" in response:
            usage = {
                "prompt_tokens": response["usage"].get("inputTokens", 0),
                "completion_tokens": response["usage"].get("outputTokens", 0),
                "total_tokens": response["usage"].get("totalTokens", 0)
            }
        
        # Handle older format responses with body field (for compatibility)
        elif isinstance(response, dict) and "body" in response:
            body = response["body"]
            
            # Handle streamingBody vs regular body
            if hasattr(body, "read"):
                # Read body content
                body_content = body.read()
                if isinstance(body_content, bytes):
                    body_content = body_content.decode('utf-8')
                
                # Parse JSON content
                if body_content:
                    try:
                        body_json = json.loads(body_content)
                        
                        # Handle different model formats
                        if "results" in body_json and len(body_json["results"]) > 0:
                            # Amazon Titan format
                            response_text = body_json["results"][0].get("outputText", "")
                        elif "content" in body_json:
                            # Anthropic Claude format
                            if isinstance(body_json["content"], str):
                                response_text = body_json["content"]
                            elif isinstance(body_json["content"], list):
                                content_pieces = []
                                for item in body_json["content"]:
                                    if isinstance(item, dict):
                                        if item.get("type") == "text":
                                            content_pieces.append(item.get("text", ""))
                                response_text = "".join(content_pieces)
                        elif "generations" in body_json and len(body_json["generations"]) > 0:
                            # Cohere format
                            response_text = body_json["generations"][0].get("text", "")
                        elif "completions" in body_json and len(body_json["completions"]) > 0:
                            # AI21 format
                            response_text = body_json["completions"][0].get("data", {}).get("text", "")
                        elif "generation" in body_json:
                            # Meta/Llama format
                            response_text = body_json["generation"]
                        elif "outputs" in body_json and len(body_json["outputs"]) > 0:
                            # Mistral format
                            response_text = body_json["outputs"][0].get("text", "")
                    except json.JSONDecodeError:
                        # If parsing fails, use the raw content
                        response_text = body_content
            
            # Handle streaming response
            elif hasattr(body, "__iter__"):
                response_chunks = []
                for event in body:
                    if "chunk" in event and "bytes" in event["chunk"]:
                        chunk_data = event["chunk"]["bytes"]
                        if isinstance(chunk_data, bytes):
                            chunk_data = chunk_data.decode('utf-8')
                        response_chunks.append(str(chunk_data))
                response_text = "".join(response_chunks)
    
    except Exception as e:
        logger.error(f"Error extracting Bedrock response content: {e}")
        logger.error(traceback.format_exc())
        response_text = f"[ERROR: Failed to extract response: {str(e)}]"
    
    return response_text, usage, function_call_info

def count_tokens_bedrock(text, model_id):
    """Estimate token count for Bedrock models based on model provider"""
    try:
        # Determine provider based on model_id
        provider = None
        for provider_name, prefixes in BEDROCK_MODEL_PREFIXES.items():
            if any(model_id.startswith(prefix) for prefix in prefixes):
                provider = provider_name
                break
        
        # Provider-specific token counting
        if provider == "anthropic":
            # Anthropic models: ~4 characters per token
            approx_tokens = len(text) // 4
            return {
                TOKEN_COUNT_KEYS["PROMPT_TOKENS"]: approx_tokens,
                TOKEN_COUNT_KEYS["COMPLETION_TOKENS"]: 0,
                TOKEN_COUNT_KEYS["TOTAL_TOKENS"]: approx_tokens
            }
        elif provider == "amazon":
            # Amazon Titan models: ~4 characters per token
            approx_tokens = len(text) // 4
            return {
                TOKEN_COUNT_KEYS["PROMPT_TOKENS"]: approx_tokens,
                TOKEN_COUNT_KEYS["COMPLETION_TOKENS"]: 0,
                TOKEN_COUNT_KEYS["TOTAL_TOKENS"]: approx_tokens
            }
        elif provider in ["meta", "mistral"]:
            # Meta/Llama and Mistral models: ~3.5 characters per token
            approx_tokens = len(text) // 3
            return {
                TOKEN_COUNT_KEYS["PROMPT_TOKENS"]: approx_tokens,
                TOKEN_COUNT_KEYS["COMPLETION_TOKENS"]: 0,
                TOKEN_COUNT_KEYS["TOTAL_TOKENS"]: approx_tokens
            }
        else:
            # Default estimation: ~4 characters per token
            approx_tokens = len(text) // 4
            return {
                TOKEN_COUNT_KEYS["PROMPT_TOKENS"]: approx_tokens,
                TOKEN_COUNT_KEYS["COMPLETION_TOKENS"]: 0,
                TOKEN_COUNT_KEYS["TOTAL_TOKENS"]: approx_tokens
            }
    
    except Exception as e:
        logger.warning(f"Failed to count tokens for Bedrock model: {e}")
        return DEFAULT_TOKEN_COUNT

def log_bedrock_call(provider, request_args, response, duration, success):
    """Log an Amazon Bedrock API call according to the unified TROPIR schema."""
    try:
        # Extract model ID early so it's available throughout the function
        model_id = request_args.get("modelId", "unknown_model")
     
        # Process request body
        body = request_args.get("body", "")
        processed_body = process_bedrock_messages(body)
        
        # If processed_body is empty but we have fields at top level, use those instead
        if not processed_body or len(processed_body) == 0:
            # Check for top-level fields that should be in the body
            top_level_fields = {}
            
            # Check for common Bedrock request fields at the top level
            for field in ["system", "inferenceConfig", "toolConfig", "messages", "inputText", "prompt"]:
                if field in request_args:
                    top_level_fields[field] = request_args[field]
            
            # If we found any top-level fields, process them
            if top_level_fields:
                processed_body = process_bedrock_messages(top_level_fields)
        
        # Create standardized request structure
        standardized_request = {
            # Rename modelId to model
            "model": model_id,
            
            # Extract inference config parameters to top level
            "temperature": request_args.get("inferenceConfig", {}).get("temperature"),
            "max_tokens": request_args.get("inferenceConfig", {}).get("maxTokens"),
            "top_p": request_args.get("inferenceConfig", {}).get("topP"),
            
            # These might be null for Bedrock, but we include them for schema consistency
            "frequency_penalty": None,
            "presence_penalty": None,
            "stop": None,
            "n": None
        }
        
        # Standardize messages structure
        messages = []
        
        # Add system message if present
        system_content = request_args.get("system", [])
        if system_content:
            if isinstance(system_content, list):
                system_text = ""
                for item in system_content:
                    if isinstance(item, dict) and "text" in item:
                        system_text += item["text"] + " "
                system_text = system_text.strip()
                
                if system_text:
                    messages.append({
                        "role": "system",
                        "content": system_text
                    })
            elif isinstance(system_content, str):
                messages.append({
                    "role": "system",
                    "content": system_content
                })
        
        # Add messages from processed_body if available
        if processed_body and "messages" in processed_body:
            for msg in processed_body.get("messages", []):
                messages.append(msg)
        elif "processed_body" in request_args and "messages" in request_args["processed_body"]:
            for msg in request_args["processed_body"].get("messages", []):
                messages.append(msg)
        
        standardized_request["messages"] = messages
        
        # Standardize tools format
        tools = []
        
        # Process toolConfig if present
        if "toolConfig" in request_args and "tools" in request_args["toolConfig"]:
            for tool in request_args["toolConfig"]["tools"]:
                if "toolSpec" in tool:
                    tool_spec = tool["toolSpec"]
                    standardized_tool = {
                        "name": tool_spec.get("name", ""),
                        "description": tool_spec.get("description", ""),
                        "parameters": {}
                    }
                    
                    # Extract parameters from inputSchema.json
                    if "inputSchema" in tool_spec and "json" in tool_spec["inputSchema"]:
                        json_schema = tool_spec["inputSchema"]["json"]
                        standardized_tool["parameters"] = {
                            "type": json_schema.get("type", "object"),
                            "properties": json_schema.get("properties", {}),
                            "required": json_schema.get("required", [])
                        }
                    
                    tools.append(standardized_tool)
        
        if tools:
            standardized_request["tools"] = tools
        
        # Generate base log entry with standardized request
        log_entry = create_base_log_entry(provider, standardized_request)
        
        # Extract response content, usage, and function call info
        response_text, usage, function_call_info = "", {}, None
        error_info = None
        
        if success:
            # Get response content for successful calls
            response_text, usage, function_call_info = extract_bedrock_response_content(response, model_id)
        else:
            # Handle error responses
            error_info = {}
            if isinstance(response, dict):
                if "error" in response:
                    error_info["error"] = response["error"]
                    response_text = f"Error: {response['error']}"
                if "ResponseMetadata" in response and "HTTPStatusCode" in response["ResponseMetadata"]:
                    error_info["status_code"] = response["ResponseMetadata"]["HTTPStatusCode"]
        
        # Standardize usage structure
        standardized_usage = {
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
            "token_details": {
                "cached_tokens": None,
                "audio_tokens": None,
                "reasoning_tokens": None,
                "accepted_prediction_tokens": None,
                "rejected_prediction_tokens": None
            }
        }
        
        # Add standardized fields to log entry
        log_entry.update({
            "response": response_text,
            "usage": standardized_usage,
            "duration": duration,
            "success": success,
        })
        
        # Standardize function call information if detected
        if function_call_info:
            # Move function call to tool_calls key
            log_entry["tool_calls"] = {
                "calls": function_call_info.get("calls", []),
                "parsed_arguments": {}
            }
            
            # Add parsed arguments if available
            for call in function_call_info.get("calls", []):
                if "function" in call and "arguments" in call["function"]:
                    try:
                        parsed_args = json.loads(call["function"]["arguments"])
                        log_entry["tool_calls"]["parsed_arguments"] = parsed_args
                    except:
                        pass
        
        # Add error information if this was a failed call
        if error_info:
            log_entry["error_info"] = error_info
        
        # Remove duplicate model_id from top level
        if "model_id" in log_entry:
            del log_entry["model_id"]
        
        # Write to log file
        send_log(log_entry)
    
    except Exception as e:
        logger.error(f"Error logging Bedrock call: {str(e)}")
        logger.error(traceback.format_exc())

def setup_bedrock_patching():
    """Set up tracking for Amazon Bedrock by patching target methods."""
    
    try:
        # Import boto3 client
        import boto3
        from botocore.client import BaseClient
        from botocore.exceptions import ClientError
        
        # Patch the BaseClient._make_api_call method to intercept Bedrock calls
        if not getattr(BaseClient, "_bedrock_patch_applied", False):
            # Store the original method
            original_make_api_call = BaseClient._make_api_call
            
            # Create the patched method
            @functools.wraps(original_make_api_call)
            def patched_make_api_call(self, operation_name, api_params):
                # Only intercept Bedrock calls
                is_bedrock_call = (
                    self._service_model.service_name == 'bedrock-runtime' and 
                    operation_name in ['InvokeModel', 'InvokeModelWithResponseStream', 'Converse']
                )
                
                # For other calls, just pass through
                if not is_bedrock_call:
                    return original_make_api_call(self, operation_name, api_params)
                
                # For Bedrock calls, wrap with tracking
                start_time = time.perf_counter()
                success = True
                response = None
                is_throttling_exception = False
                
                try:
                    # Call the original method
                    response = original_make_api_call(self, operation_name, api_params)
                    return response
                except ClientError as e:
                    success = False
                    response = {"error": str(e)}
                    
                    # Check if this is a ThrottlingException
                    error_code = e.response.get('Error', {}).get('Code', '')
                    if error_code == 'ThrottlingException':
                        is_throttling_exception = True
                        logger.warning(f"ThrottlingException detected, skipping logging: {str(e)}")
                    
                    raise
                except Exception as e:
                    success = False
                    response = {"error": str(e)}
                    raise
                finally:
                    # Only log if we have params and it's not a ThrottlingException
                    if api_params and not is_throttling_exception:
                        duration = time.perf_counter() - start_time
                        try:
                            log_bedrock_call("bedrock", api_params, response, duration, success)
                        except Exception as log_error:
                            logger.error(f"Error logging Bedrock call: {log_error}")
            
            # Apply the patch
            BaseClient._make_api_call = patched_make_api_call
            BaseClient._bedrock_patch_applied = True
    
    except ImportError:
        logger.warning("Could not import 'boto3'. Bedrock tracking will not work.")
    except Exception as e:
        logger.error(f"Failed during Amazon Bedrock patching process: {e}")
        logger.error(traceback.format_exc())
