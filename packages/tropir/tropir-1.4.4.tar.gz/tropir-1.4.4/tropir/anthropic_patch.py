"""
Anthropic-specific patching logic for LLM tracking.
"""

import functools
import time
import traceback
import json
import os
import uuid
from datetime import datetime
from loguru import logger

from tropir.transport import send_log

from .constants import (
    TOKEN_COUNT_KEYS,
    DEFAULT_TOKEN_COUNT,
    ANTHROPIC_MODEL_PREFIXES
)
from .utils import (
    create_base_log_entry,
    create_generic_method_wrapper,
    create_async_method_wrapper,
)

def process_anthropic_messages(messages):
    """Process Anthropic messages to handle special content types"""
    processed_messages = []
    for msg in messages:
        if isinstance(msg, dict) or hasattr(msg, "keys"):
            # Convert frozendict to dict if needed
            msg_dict = dict(msg) if not isinstance(msg, dict) else msg
            processed_msg = msg_dict.copy()
            content = msg_dict.get("content")

            # Handle list-type content (multimodal messages)
            if isinstance(content, list):
                processed_content = []
                for item in content:
                    if isinstance(item, dict):
                        item_copy = item.copy()
                        # Handle Anthropic image types
                        if item_copy.get("type") == "image" and "source" in item_copy:
                            source = item_copy["source"]
                            if isinstance(source, dict) and "data" in source:
                                if source.get("media_type", "").startswith("image/"):
                                    item_copy["source"]["data"] = "[BASE64_IMAGE_REMOVED]"
                        processed_content.append(item_copy)
                    else:
                        processed_content.append(item)
                processed_msg["content"] = processed_content
            elif isinstance(content, str):
                # Strip leading and trailing newlines from string content
                processed_msg["content"] = content.strip('\n')

            processed_messages.append(processed_msg)
        else:
            # Handle non-dict message objects
            try:
                # For Anthropic message objects
                if hasattr(msg, "type") and hasattr(msg, "role"):
                    # This is likely an Anthropic message
                    role = getattr(msg, "role", "unknown")
                    content = getattr(msg, "content", "")
                    
                    # Process content if it's a list (multi-modal or tool calls)
                    if isinstance(content, list):
                        processed_content = []
                        for item in content:
                            if hasattr(item, "type"):
                                item_type = getattr(item, "type")
                                if item_type == "text" and hasattr(item, "text"):
                                    processed_content.append({
                                        "type": "text",
                                        "text": getattr(item, "text", "").strip('\n')
                                    })
                                elif item_type == "image" and hasattr(item, "source"):
                                    source = getattr(item, "source")
                                    if hasattr(source, "data") and hasattr(source, "media_type"):
                                        # Don't include actual image data
                                        processed_content.append({
                                            "type": "image",
                                            "source": {
                                                "media_type": getattr(source, "media_type", ""),
                                                "data": "[BASE64_IMAGE_REMOVED]"
                                            }
                                        })
                                elif item_type == "tool_use" and hasattr(item, "tool_use"):
                                    tool_use = getattr(item, "tool_use")
                                    processed_content.append({
                                        "type": "tool_use",
                                        "tool_use": {
                                            "name": getattr(tool_use, "name", ""),
                                            "input": getattr(tool_use, "input", {})
                                        }
                                    })
                        processed_messages.append({
                            "role": role,
                            "content": processed_content
                        })
                    else:
                        # For simple string content
                        if isinstance(content, str):
                            content = content.strip('\n')
                        processed_messages.append({
                            "role": role,
                            "content": content
                        })
                else:
                    # Generic object handling
                    processed_messages.append({
                        "role": getattr(msg, "role", "unknown"),
                        "content": str(getattr(msg, "content", str(msg)))
                    })
            except Exception as e:
                # If all else fails, create a basic message
                logger.warning(f"Error processing Anthropic message object: {e}")
                processed_messages.append({
                    "role": getattr(msg, "role", "unknown"),
                    "content": str(getattr(msg, "content", str(msg)))
                })

    return processed_messages

def count_tokens_anthropic(text, model):
    """Count tokens in text specifically for Anthropic models"""
    try:
        # Try to use Anthropic's built-in token counter
        from anthropic import Anthropic
        client = Anthropic()
        token_count = client.count_tokens(text)
        return {
            TOKEN_COUNT_KEYS["PROMPT_TOKENS"]: token_count,
            TOKEN_COUNT_KEYS["COMPLETION_TOKENS"]: 0,
            TOKEN_COUNT_KEYS["TOTAL_TOKENS"]: token_count
        }
    except (ImportError, AttributeError) as e:
        # Fallback to approximate counting for Anthropic models
        # Claude models use roughly ~4 characters per token on average
        logger.warning(f"Using approximate token counting for Anthropic: {e}")
        approx_tokens = len(text) // 4
        return {
            TOKEN_COUNT_KEYS["PROMPT_TOKENS"]: approx_tokens,
            TOKEN_COUNT_KEYS["COMPLETION_TOKENS"]: 0,
            TOKEN_COUNT_KEYS["TOTAL_TOKENS"]: approx_tokens
        }
    except Exception as e:
        logger.warning(f"Failed to count tokens for Anthropic model: {e}")
        return DEFAULT_TOKEN_COUNT

def log_anthropic_call(provider, request_args, response, duration, success):
    """Log an Anthropic LLM API call according to the unified TROPIR schema."""
    try:
        # Extract messages from request_args
        messages = request_args.get("messages", [])
        processed_messages = process_anthropic_messages(messages)
        
        # Add system message if present as a separate field
        if request_args.get("system") and not any(msg.get("role") == "system" for msg in processed_messages):
            processed_messages = [{"role": "system", "content": request_args["system"]}] + processed_messages

        # Prepare standardized request structure
        standardized_request = {
            "model": request_args.get("model", ""),
            "messages": processed_messages,
            "temperature": request_args.get("temperature"),
            "max_tokens": request_args.get("max_tokens"),
            "top_p": request_args.get("top_p"),
            "frequency_penalty": None,  # Anthropic doesn't use these, but we include for schema consistency
            "presence_penalty": None,
            "stop": request_args.get("stop", None),
            "n": None
        }
        
        # Standardize tools format if present
        if "tools" in request_args:
            standardized_tools = []
            for tool in request_args.get("tools", []):
                standardized_tool = {
                    "name": tool.get("name", ""),
                    "description": tool.get("description", ""),
                    "parameters": {}
                }
                
                # Convert input_schema to parameters
                if "input_schema" in tool:
                    input_schema = tool["input_schema"]
                    standardized_tool["parameters"] = {
                        "type": input_schema.get("type", "object"),
                        "properties": input_schema.get("properties", {}),
                        "required": input_schema.get("required", [])
                    }
                
                standardized_tools.append(standardized_tool)
            
            if standardized_tools:
                standardized_request["tools"] = standardized_tools

        response_text = ""
        usage = {}
        function_call_info = None
        reasoning = None
        model = standardized_request.get("model", "")
        
        # Check for stored JSON data on HTTP response objects
        response_json = None
        if hasattr(response, '_tropir_json_data'):
            response_json = response._tropir_json_data
        elif hasattr(response, 'status_code') and hasattr(response, 'json') and callable(response.json):
            try:
                response_json = response.json()
            except Exception as e:
                logger.warning(f"Failed to get JSON from HTTP response: {e}")
                
        # Process HTTP response with JSON data
        if response_json:
            # Extract content from Anthropic API response
            if "content" in response_json:
                # For newer API versions that return a list of content blocks
                if isinstance(response_json["content"], list):
                    text_blocks = []
                    tool_calls = []
                    
                    for block in response_json["content"]:
                        if block.get("type") == "text":
                            text_content = block.get("text", "")
                            if text_content:
                                text_blocks.append(text_content)
                        elif block.get("type") == "thinking":
                            # Extract reasoning from thinking block
                            thinking_content = block.get("thinking", "")
                            if thinking_content:
                                reasoning = thinking_content
                        elif block.get("type") == "tool_use":
                            # Extract tool information
                            tool_use = block.get("tool_use", {})
                            if not tool_use and block.get("name") and block.get("input"):
                                # Direct structure in older versions
                                tool_name = block.get("name", "unknown")
                                tool_input = block.get("input", {})
                            else:
                                # Newer structure with tool_use object
                                tool_name = tool_use.get("name", block.get("name", "unknown"))
                                tool_input = tool_use.get("input", block.get("input", {}))
                            
                            # Create standardized tool call
                            tool_call = {
                                "id": block.get("id", str(uuid.uuid4())),
                                "type": "function",
                                "function": {
                                    "name": tool_name,
                                    "arguments": json.dumps(tool_input)
                                }
                            }
                            tool_calls.append(tool_call)
                            
                            # Add formatted tool call to text blocks
                            try:
                                # Format the tool input for better readability
                                formatted_input = json.dumps(tool_input, indent=2)
                                tool_text = f"\n[TOOL_CALL: {tool_name}]\n{formatted_input}"
                                text_blocks.append(tool_text)
                            except:
                                # Fallback if formatting fails
                                text_blocks.append(f"\n[TOOL_CALL: {tool_name}]")
                    
                    # Join text blocks
                    if text_blocks:
                        response_text = "\n".join(text_blocks)
                    
                    # Store tool calls
                    if tool_calls:
                        function_call_info = {
                            "calls": tool_calls,
                            "parsed_arguments": {}
                        }
                        
                        # Try to extract arguments from the first tool call
                        if tool_calls:
                            try:
                                first_call = tool_calls[0]
                                args_json = first_call["function"]["arguments"]
                                function_call_info["parsed_arguments"] = json.loads(args_json)
                            except:
                                pass
            
            # Extract usage information if available
            if "usage" in response_json:
                usage = {
                    "prompt_tokens": response_json["usage"].get("input_tokens", 0),
                    "completion_tokens": response_json["usage"].get("output_tokens", 0),
                    "total_tokens": (
                        response_json["usage"].get("input_tokens", 0) +
                        response_json["usage"].get("output_tokens", 0)
                    )
                }
        
        # Process Anthropic response
        elif success and response and not isinstance(response, dict):
            # Extract usage information if available
            if hasattr(response, "usage"):
                usage = {
                    "prompt_tokens": getattr(response.usage, "input_tokens", 0),
                    "completion_tokens": getattr(response.usage, "output_tokens", 0),
                    "total_tokens": getattr(response.usage, "input_tokens", 0) + getattr(response.usage, "output_tokens", 0)
                }
            
            # Handle content blocks from the response
            if hasattr(response, "content"):
                tool_calls = []
                text_blocks = []
                
                for block in response.content:
                    if hasattr(block, "type"):
                        if block.type == "text":
                            text_content = getattr(block, "text", "") 
                            if text_content:
                                text_blocks.append(text_content)
                        elif block.type == "thinking":
                            # Extract reasoning from thinking block
                            thinking_content = getattr(block, "thinking", "")
                            if thinking_content:
                                reasoning = thinking_content
                        elif block.type == "tool_use":
                            # Extract tool information directly from the block
                            # The Anthropic API has 'name' and 'input' at the top level of the tool_use block
                            tool_call = {
                                "id": getattr(block, "id", str(uuid.uuid4())),
                                "type": "function",
                                "function": {
                                    "name": getattr(block, "name", "unknown"),
                                    "arguments": json.dumps(getattr(block, "input", {}))
                                }
                            }
                            tool_calls.append(tool_call)
                            
                            # Add formatted tool call to text blocks
                            tool_name = getattr(block, "name", "unknown")
                            tool_input = getattr(block, "input", {})
                            try:
                                # Format the tool input for better readability
                                formatted_input = json.dumps(tool_input, indent=2)
                                tool_text = f"\n[TOOL_CALL: {tool_name}]\n{formatted_input}"
                                text_blocks.append(tool_text)
                            except:
                                # Fallback if formatting fails
                                text_blocks.append(f"\n[TOOL_CALL: {tool_name}]")
                
                # Combine all text blocks
                if text_blocks:
                    response_text = "\n".join(text_blocks)
                
                # If tool calls were found, save them for tool_calls field
                if tool_calls:
                    function_call_info = {
                        "calls": tool_calls
                    }
                    
                    # Try to extract arguments from the first tool call
                    if tool_calls:
                        try:
                            first_call = tool_calls[0]
                            args_json = first_call["function"]["arguments"]
                            function_call_info["parsed_arguments"] = json.loads(args_json)
                        except:
                            function_call_info["parsed_arguments"] = {}
                    
                    # If we didn't get any content text, create a placeholder
                    if not response_text:
                        response_text = f"[TOOL_CALLS: {len(tool_calls)}]"

        # Try to extract content from dictionary response (likely error case or direct API call)
        elif isinstance(response, dict):
            # Handle error responses
            if "error" in response:
                response_text = response.get("error", {}).get("message", str(response))
                usage = {}
            # Handle successful direct API responses
            elif "content" in response:
                text_blocks = []
                tool_calls = []
                
                for block in response.get("content", []):
                    if isinstance(block, dict):
                        if block.get("type") == "text":
                            text_blocks.append(block.get("text", ""))
                        elif block.get("type") == "thinking":
                            # Extract reasoning from thinking block
                            thinking_content = block.get("thinking", "")
                            if thinking_content:
                                reasoning = thinking_content
                        elif block.get("type") == "tool_use":
                            # Extract tool information directly from the block
                            tool_use = block.get("tool_use", {})
                            if not tool_use and block.get("name") and block.get("input"):
                                # Direct structure in older versions
                                tool_name = block.get("name", "unknown")
                                tool_input = block.get("input", {})
                            else:
                                # Newer structure with tool_use object
                                tool_name = tool_use.get("name", block.get("name", "unknown"))
                                tool_input = tool_use.get("input", block.get("input", {}))
                            
                            # Create standardized tool call
                            tool_call = {
                                "id": block.get("id", str(uuid.uuid4())),
                                "type": "function",
                                "function": {
                                    "name": tool_name,
                                    "arguments": json.dumps(tool_input)
                                }
                            }
                            tool_calls.append(tool_call)
                            
                            # Add formatted tool call to text blocks
                            try:
                                # Format the tool input for better readability
                                formatted_input = json.dumps(tool_input, indent=2)
                                tool_text = f"\n[TOOL_CALL: {tool_name}]\n{formatted_input}"
                                text_blocks.append(tool_text)
                            except:
                                # Fallback if formatting fails
                                text_blocks.append(f"\n[TOOL_CALL: {tool_name}]")
                
                # Combine all text blocks
                response_text = "\n".join(text_blocks) if text_blocks else ""
                
                # If tool calls were found, save them for function_call_info
                if tool_calls:
                    function_call_info = {
                        "calls": tool_calls
                    }
                    
                    # Try to extract arguments from the first tool call
                    if tool_calls:
                        try:
                            first_call = tool_calls[0]
                            args_json = first_call["function"]["arguments"]
                            function_call_info["parsed_arguments"] = json.loads(args_json)
                        except:
                            function_call_info["parsed_arguments"] = {}
                    
                    # If we didn't get any content text, create a placeholder
                    if not response_text:
                        response_text = f"[TOOL_CALLS: {len(tool_calls)}]"
                
                # Extract usage information
                usage = response.get("usage", {})
                # Adjust key names if necessary (direct API uses input_tokens/output_tokens)
                if "input_tokens" in usage:
                    usage = {
                        "prompt_tokens": usage.get("input_tokens", 0),
                        "completion_tokens": usage.get("output_tokens", 0),
                        "total_tokens": usage.get("input_tokens", 0) + usage.get("output_tokens", 0)
                    }
            else:
                # Handle other dictionary response formats
                response_text = str(response)
                usage = response.get("usage", {})
        
        # Count tokens if not provided
        if not usage:
            # Determine if we should use Anthropic-specific token counting
            use_anthropic_counting = any(model.startswith(prefix) for prefix in ANTHROPIC_MODEL_PREFIXES)
            
            if use_anthropic_counting:
                # Join messages to count prompt tokens
                prompt_text = " ".join(str(msg.get("content", "")) for msg in messages if msg.get("content"))
                
                # Count completion tokens
                resp_text_str = str(response_text) if response_text else ""
                
                # Count tokens using Anthropic-specific method
                prompt_tokens = count_tokens_anthropic(prompt_text, model)
                completion_tokens = count_tokens_anthropic(resp_text_str, model) if resp_text_str else DEFAULT_TOKEN_COUNT
                
                usage = {
                    "prompt_tokens": prompt_tokens.get(TOKEN_COUNT_KEYS["PROMPT_TOKENS"], 0),
                    "completion_tokens": completion_tokens.get(TOKEN_COUNT_KEYS["COMPLETION_TOKENS"], 0),
                    "total_tokens": (
                        prompt_tokens.get(TOKEN_COUNT_KEYS["PROMPT_TOKENS"], 0) + 
                        completion_tokens.get(TOKEN_COUNT_KEYS["COMPLETION_TOKENS"], 0)
                    )
                }
            else:
                # Fallback to basic token counting (very rough estimation)
                prompt_text = " ".join(str(msg.get("content", "")) for msg in messages if msg.get("content"))
                resp_text_str = str(response_text) if response_text else ""
                usage = {
                    "prompt_tokens": len(prompt_text) // 4,  # Very rough approximation
                    "completion_tokens": len(resp_text_str) // 4,
                    "total_tokens": (len(prompt_text) + len(resp_text_str)) // 4
                }
        
        # Standardize the usage structure with token_details
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

        # Generate log entry with standardized request
        log_entry = create_base_log_entry(provider, standardized_request)
        
        # Add remaining fields
        log_entry.update({
            "response": response_text,
            "usage": standardized_usage,
            "duration": duration,
            "success": success,
        })
        
        # Add reasoning if present
        if reasoning:
            log_entry["reasoning"] = reasoning
        
        # Convert function_call to tool_calls format with parsed arguments
        if function_call_info:
            parsed_arguments = function_call_info.get("parsed_arguments", {})
            
            # If parsed_arguments wasn't set, try to parse arguments from any tool calls
            if not parsed_arguments and "calls" in function_call_info:
                for call in function_call_info.get("calls", []):
                    if "function" in call and "arguments" in call["function"]:
                        try:
                            args_json = call["function"]["arguments"]
                            parsed_args = json.loads(args_json)
                            # If this is the first tool call, use its parsed arguments
                            if not parsed_arguments:
                                parsed_arguments = parsed_args
                        except json.JSONDecodeError:
                            logger.warning(f"Failed to parse tool call arguments: {args_json}")
            
            log_entry["tool_calls"] = {
                "calls": function_call_info.get("calls", []),
                "parsed_arguments": parsed_arguments
            }
        
        # Remove any leftover function_call field if it exists (to be consistent with schema)
        if "function_call" in log_entry:
            del log_entry["function_call"]

        # Remove duplicate model_id from top level
        if "model_id" in log_entry:
            del log_entry["model_id"]
        
        # Write to log file
        send_log(log_entry)

    except Exception as e:
        logger.error(f"Error logging Anthropic call: {str(e)}")
        logger.error(traceback.format_exc())

def patched_requests_post(original_post, *args, **kwargs):
    """
    Patched version of requests.post to track direct HTTP calls to Anthropic API.
    """
    url = args[0] if args else kwargs.get('url')
    
    # Only process specific Anthropic API endpoints to avoid interfering with SDK
    is_anthropic_api = (
        url and 
        isinstance(url, str) and 
        (
            # More inclusive matching for Anthropic API calls
            "api.anthropic.com" in url or
            "claude-api.ai" in url
        )
    )
    
    if is_anthropic_api:
        try:
            logger.debug(f"Intercepted direct API call to Anthropic endpoint: {url}")
            start_time = time.time()
            success = True
            
            # Handle both JSON and data parameters
            if 'json' in kwargs:
                request_data = kwargs.get('json', {})
            elif 'data' in kwargs:
                # Try to parse data if it's a JSON string
                data = kwargs.get('data', '{}')
                if isinstance(data, str):
                    try:
                        request_data = json.loads(data)
                    except:
                        request_data = {'data': data}
                else:
                    request_data = {'data': data}
            else:
                request_data = {}
            
            # Make the actual request
            try:
                response = original_post(*args, **kwargs)
                
                # Extract JSON data from the response before passing to log function
                # This is critical for proper content extraction
                try:
                    response_data = response.json()
                    # Save the JSON data on the response object for later use
                    response._tropir_json_data = response_data
                    success = response.status_code < 400
                except Exception as json_error:
                    logger.error(f"Failed to parse JSON from Anthropic response: {json_error}")
                    response_data = {"error": {"message": f"Failed to parse response: {str(json_error)}"}}
                    success = False
            except Exception as e:
                success = False
                response_data = {"error": {"message": str(e)}}
                response = None
                logger.error(f"Error making Anthropic HTTP request: {str(e)}")
                raise
            finally:
                duration = time.time() - start_time
                
                # Only log if this wasn't already logged by the SDK
                # This is a key improvement to avoid duplicate logging
                if not getattr(request_data, '_tropir_logged', False):
                    logger.info(f"Logging direct Anthropic API call to: {url}")
                    
                    # Use the response object rather than just the JSON data
                    # This allows log_anthropic_call to access _tropir_json_data
                    log_anthropic_call("anthropic", request_data, response, duration, success)
                    
                    # Mark as logged to prevent double-logging
                    if isinstance(request_data, dict):
                        request_data['_tropir_logged'] = True
            
            return response
        except Exception as e:
            logger.error(f"Error in patched requests.post for Anthropic: {str(e)}")
            logger.error(traceback.format_exc())
            # Always let the original request proceed even if tracking fails
            return original_post(*args, **kwargs)
    else:
        # For non-Anthropic URLs, just call the original function
        return original_post(*args, **kwargs)

async def patched_httpx_async_post(original_post, self, url, *args, **kwargs):
    """
    Patched version of httpx.AsyncClient.post to track direct HTTP calls to Anthropic API.
    """
    # Only process specific Anthropic API endpoints to avoid interfering with SDK
    is_anthropic_api = (
        url and 
        isinstance(url, str) and 
        (
            # More inclusive matching for Anthropic API calls
            "api.anthropic.com" in url or
            "claude-api.ai" in url
        )
    )
    
    if is_anthropic_api:
        try:
            logger.debug(f"Intercepted direct async API call to Anthropic endpoint: {url}")
            start_time = time.time()
            success = True
            
            # Handle both JSON and data parameters
            if 'json' in kwargs:
                request_data = kwargs.get('json', {})
            elif 'data' in kwargs:
                # Try to parse data if it's a JSON string
                data = kwargs.get('data', '{}')
                if isinstance(data, str):
                    try:
                        request_data = json.loads(data)
                    except:
                        request_data = {'data': data}
                else:
                    request_data = {'data': data}
            else:
                request_data = {}
            
            # Make the actual request
            try:
                response = await original_post(self, url, *args, **kwargs)
                
                # Extract JSON data from the response before passing to log function
                # This is critical for proper content extraction
                try:
                    response_data = response.json()
                    # Save the JSON data on the response object for later use
                    response._tropir_json_data = response_data
                    success = response.status_code < 400
                except Exception as json_error:
                    logger.error(f"Failed to parse JSON from Anthropic response: {json_error}")
                    response_data = {"error": {"message": f"Failed to parse response: {str(json_error)}"}}
                    success = False
            except Exception as e:
                success = False
                response_data = {"error": {"message": str(e)}}
                response = None
                logger.error(f"Error making Anthropic HTTP request: {str(e)}")
                raise
            finally:
                duration = time.time() - start_time
                
                # Only log if this wasn't already logged by the SDK
                # This is a key improvement to avoid duplicate logging
                if not getattr(request_data, '_tropir_logged', False):
                    logger.info(f"Logging direct Anthropic API call to: {url}")
                    
                    # Add URL to request data for proper logging
                    if isinstance(request_data, dict):
                        request_data["url"] = url
                    
                    # Use the response object rather than just the JSON data
                    # This allows log_anthropic_call to access _tropir_json_data
                    log_anthropic_call("anthropic", request_data, response, duration, success)
                    
                    # Mark as logged to prevent double-logging
                    if isinstance(request_data, dict):
                        request_data['_tropir_logged'] = True
            
            return response
        except Exception as e:
            logger.error(f"Error in patched httpx.AsyncClient.post for Anthropic: {str(e)}")
            logger.error(traceback.format_exc())
            # Always let the original request proceed even if tracking fails
            return await original_post(self, url, *args, **kwargs)
    else:
        # For non-Anthropic URLs, just call the original function
        return await original_post(self, url, *args, **kwargs)

def setup_http_patching():
    """Set up tracking specifically for direct HTTP calls to Anthropic API."""
    try:
        # Patch requests library for synchronous HTTP calls
        try:
            import requests
            if not getattr(requests.post, '_llm_tracker_patched_anthropic_http', False):
                logger.info("Patching requests.post for direct Anthropic API calls")
                original_post = requests.post
                
                # Create a wrapper that maintains the function signature
                @functools.wraps(original_post)
                def wrapper(*args, **kwargs):
                    return patched_requests_post(original_post, *args, **kwargs)
                
                # Mark as patched with a specific tag for HTTP patching
                wrapper._llm_tracker_patched_anthropic_http = True
                requests.post = wrapper
                logger.info("Successfully patched requests.post for direct Anthropic API calls")
            else:
                logger.info("requests.post already patched for direct Anthropic API calls")
        except ImportError:
            logger.debug("Could not import 'requests'. Direct HTTP patching for requests will be skipped.")
            
        # Patch httpx.AsyncClient for async HTTP calls
        try:
            import httpx
            if not getattr(httpx.AsyncClient.post, '_llm_tracker_patched_anthropic_http', False):
                logger.info("Patching httpx.AsyncClient.post for direct Anthropic API calls")
                original_async_post = httpx.AsyncClient.post
                
                # Create an async wrapper that maintains the function signature
                @functools.wraps(original_async_post)
                async def async_wrapper(self, url, *args, **kwargs):
                    return await patched_httpx_async_post(original_async_post, self, url, *args, **kwargs)
                
                # Mark as patched with a specific tag for HTTP patching
                async_wrapper._llm_tracker_patched_anthropic_http = True
                httpx.AsyncClient.post = async_wrapper
                logger.info("Successfully patched httpx.AsyncClient.post for direct Anthropic API calls")
            else:
                logger.info("httpx.AsyncClient.post already patched for direct Anthropic API calls")
        except ImportError:
            logger.debug("Could not import 'httpx'. Direct HTTP patching for httpx will be skipped.")
            
    except Exception as e:
        logger.error(f"Failed to set up HTTP patching for Anthropic: {e}")
        logger.error(traceback.format_exc())

def setup_anthropic_patching():
    """Set up tracking for Anthropic by patching target methods."""
    try:
        # Try to import and patch the SDK first
        try:
            from anthropic.resources.messages import Messages
            from anthropic.resources.messages import AsyncMessages
            
            # Patch synchronous Messages.create
            if hasattr(Messages, "create") and not getattr(Messages.create, '_llm_tracker_patched', False):
                original_messages_create = Messages.create
                
                # Create the wrapped version using our helper function
                patched_messages_create = create_generic_method_wrapper(
                    original_messages_create, 
                    "anthropic", 
                    log_anthropic_call
                )
                
                # Replace the original method with the patched one
                Messages.create = patched_messages_create
                Messages.create._llm_tracker_patched = True
                logger.info("Successfully patched Anthropic Messages.create")
            elif hasattr(Messages, "create") and getattr(Messages.create, '_llm_tracker_patched', False):
                logger.debug("Anthropic Messages.create already patched.")
            else:
                logger.warning("Could not find 'create' method on Anthropic Messages class for patching.")
            
            # Patch asynchronous AsyncMessages.create
            if hasattr(AsyncMessages, "create") and not getattr(AsyncMessages.create, '_llm_tracker_patched', False):
                original_async_messages_create = AsyncMessages.create
                
                # Create an async-compatible wrapped version
                patched_async_messages_create = create_async_method_wrapper(
                    original_async_messages_create, 
                    "anthropic", 
                    log_anthropic_call
                )
                
                # Replace the original method with the patched one
                AsyncMessages.create = patched_async_messages_create
                AsyncMessages.create._llm_tracker_patched = True
                logger.info("Successfully patched Anthropic AsyncMessages.create")
            elif hasattr(AsyncMessages, "create") and getattr(AsyncMessages.create, '_llm_tracker_patched', False):
                logger.debug("Anthropic AsyncMessages.create already patched.")
            else:
                logger.warning("Could not find 'create' method on Anthropic AsyncMessages class for patching.")
                
        except ImportError:
            logger.warning("Could not import 'anthropic.resources.messages'. Only direct API calls will be tracked.")
        
        # Now setup HTTP patching - do this separately to avoid interference
        setup_http_patching()
        
    except Exception as e:
        logger.error(f"Failed during Anthropic patching process: {e}")
        logger.error(traceback.format_exc())