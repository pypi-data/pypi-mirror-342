"""
OpenRouter-specific patching logic for LLM tracking.
"""

import functools
import time
import traceback
import json
import os
import uuid
import requests
from datetime import datetime
from loguru import logger

from .constants import (
    TOKEN_COUNT_KEYS,
    DEFAULT_TOKEN_COUNT
)
from .transport import send_log
from .utils import (
    create_base_log_entry,
    create_generic_method_wrapper,
    create_async_method_wrapper,
)

def is_openrouter_url(url):
    """Check if a URL is an OpenRouter API endpoint"""
    return url and isinstance(url, str) and "openrouter.ai/api" in url

def is_openrouter_request(base_url=None, url=None, api_base=None, client=None):
    """More comprehensive check for OpenRouter requests"""
    # Check base_url parameter
    if is_openrouter_url(base_url):
        return True
        
    # Check url parameter
    if is_openrouter_url(url):
        return True
        
    # Check api_base parameter
    if is_openrouter_url(api_base):
        return True
        
    # Check client's base_url
    if client and hasattr(client, "base_url") and is_openrouter_url(client.base_url):
        return True
        
    # Check self._client.base_url if self is an object with _client attribute
    if client and hasattr(client, "_client") and hasattr(client._client, "base_url"):
        if is_openrouter_url(client._client.base_url):
            return True
            
    return False

def is_openrouter_model_format(model):
    """Check if a model string follows OpenRouter format (provider/model)"""
    if model and isinstance(model, str) and "/" in model:
        model_parts = model.split("/")
        if len(model_parts) >= 2 and model_parts[0] in ["openai", "anthropic", "google", "meta", "cohere"]:
            return True
    return False

def process_messages(messages):
    """Process OpenAI messages to handle special content types"""
    processed_messages = []
    
    # Debug input messages
    logger.debug(f"Processing messages input (type: {type(messages)}): {messages}")
    
    # Handle single string input (responses.create input parameter)
    if isinstance(messages, str):
        return [{"role": "user", "content": messages.strip('\n')}]
    
    # Handle input parameter with instructions from responses.create
    if isinstance(messages, dict) and "input" in messages and isinstance(messages["input"], str):
        result = []
        if "instructions" in messages and messages["instructions"]:
            result.append({"role": "system", "content": messages["instructions"].strip('\n')})
        result.append({"role": "user", "content": messages["input"].strip('\n')})
        return result
        
    # Handle input list format from responses.create
    if isinstance(messages, list) and messages and isinstance(messages[0], dict) and "role" in messages[0] and "content" in messages[0]:
        result = []
        for msg in messages:
            # Force into a standard format
            new_msg = {
                "role": msg.get("role", "user"),
                "content": msg.get("content", "").strip('\n') if isinstance(msg.get("content"), str) else msg.get("content")
            }
            
            # Add tool calls if present
            if "tool_calls" in msg:
                new_msg["tool_calls"] = msg["tool_calls"]
                
            # Add tool_call_id if present
            if "tool_call_id" in msg:
                new_msg["tool_call_id"] = msg["tool_call_id"]
                
            # Add name if present (for tool responses)
            if "name" in msg:
                new_msg["name"] = msg["name"]
                
            result.append(new_msg)
        return result
    
    # Original processing logic for standard messages format
    for idx, msg in enumerate(messages):
        logger.debug(f"Processing message {idx}: {type(msg)}")
        
        if isinstance(msg, dict) or hasattr(msg, "keys"):
            # Convert frozendict to dict if needed
            msg_dict = dict(msg) if not isinstance(msg, dict) else msg
            processed_msg = msg_dict.copy()
            
            # Debug assistant message
            if msg_dict.get("role") == "assistant":
                logger.debug(f"Processing assistant message: {msg_dict}")
                
            content = msg_dict.get("content")

            # Handle list-type content (multimodal messages)
            if isinstance(content, list):
                processed_content = []
                for item in content:
                    if isinstance(item, dict):
                        item_copy = item.copy()
                        # Handle image types in OpenAI messages
                        if "image_url" in item_copy:
                            url = item_copy["image_url"].get("url", "")
                            if url and url.startswith("data:image"):
                                item_copy["image_url"]["url"] = "[BASE64_IMAGE_REMOVED]"
                        processed_content.append(item_copy)
                    else:
                        processed_content.append(item)
                processed_msg["content"] = processed_content
            elif isinstance(content, str):
                # Strip leading and trailing newlines from string content
                processed_msg["content"] = content.strip('\n')

            # Handle tool calls in assistant messages
            if msg_dict.get("role") == "assistant" and "tool_calls" in msg_dict:
                tool_calls = msg_dict["tool_calls"]
                processed_tool_calls = []
                
                logger.debug(f"Found tool_calls in assistant message: {tool_calls}")
                
                for tool in tool_calls:
                    if not isinstance(tool, dict):
                        # Convert non-dict tool calls to dict
                        if hasattr(tool, "id") and hasattr(tool, "function"):
                            tool = {
                                "id": tool.id,
                                "type": getattr(tool, "type", "function"),
                                "function": {
                                    "name": tool.function.name if hasattr(tool.function, "name") else "unknown_function",
                                    "arguments": tool.function.arguments if hasattr(tool.function, "arguments") else "{}"
                                }
                            }
                        else:
                            # If we can't convert, create a minimal placeholder
                            tool = {"id": str(uuid.uuid4()), "type": "function", "function": {"name": "unknown", "arguments": "{}"}}
                            
                    tool_details = {
                        "id": tool.get("id", f"call_{uuid.uuid4().hex[:8]}"),
                        "type": tool.get("type", "function"),
                        "function": {
                            "name": tool.get("function", {}).get("name", "unknown_function"),
                            "arguments": tool.get("function", {}).get("arguments", "{}")
                        }
                    }
                    processed_tool_calls.append(tool_details)
                
                processed_msg["tool_calls"] = processed_tool_calls

            # Handle tool results
            if msg_dict.get("role") == "tool":
                processed_msg["tool_call_id"] = msg_dict.get("tool_call_id")
                processed_msg["name"] = msg_dict.get("name")

            processed_messages.append(processed_msg)
        else:
            # Handle non-dict message objects by extracting key properties
            try:
                # Create a base message dict
                processed_msg = {
                    "role": getattr(msg, "role", "unknown")
                }
                
                # Handle content property
                if hasattr(msg, "content"):
                    content = msg.content
                    if isinstance(content, str):
                        processed_msg["content"] = content.strip('\n')
                    else:
                        processed_msg["content"] = content
                else:
                    processed_msg["content"] = str(msg)
                
                # Add tool calls if present
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    logger.debug(f"Processing tool_calls from object: {msg.tool_calls}")
                    
                    tool_calls = []
                    for t in msg.tool_calls:
                        if hasattr(t, "model_dump"):
                            tool_calls.append(t.model_dump())
                        elif hasattr(t, "to_dict"):
                            tool_calls.append(t.to_dict())
                        elif hasattr(t, "__dict__"):
                            # Extract the key attributes manually
                            tool_call = {
                                "id": getattr(t, "id", str(uuid.uuid4())),
                                "type": getattr(t, "type", "function"),
                                "function": {}
                            }
                            
                            # Extract function details
                            if hasattr(t, "function"):
                                fn = t.function
                                tool_call["function"] = {
                                    "name": getattr(fn, "name", "unknown"),
                                    "arguments": getattr(fn, "arguments", "{}")
                                }
                            
                            tool_calls.append(tool_call)
                        else:
                            # Last resort: try to convert to string
                            tool_calls.append(str(t))
                    
                    processed_msg["tool_calls"] = tool_calls
                
                # Add tool call ID if present (for tool results)
                if hasattr(msg, "tool_call_id"):
                    processed_msg["tool_call_id"] = msg.tool_call_id
                
                # Add name if present (for functions/tools)
                if hasattr(msg, "name"):
                    processed_msg["name"] = msg.name
                
                processed_messages.append(processed_msg)
                logger.debug(f"Processed message object to: {processed_msg}")
            except Exception as e:
                # If all else fails, create a basic message
                logger.warning(f"Error processing message object: {e}")
                logger.warning(f"Message type: {type(msg)}, dir: {dir(msg)}")
                try:
                    processed_messages.append({
                        "role": getattr(msg, "role", "unknown"),
                        "content": str(getattr(msg, "content", str(msg)))
                    })
                except Exception as e2:
                    logger.error(f"Failed to fallback process message: {e2}")
                    # Ultimate fallback
                    processed_messages.append({
                        "role": "unknown",
                        "content": f"[UNPARSEABLE_MESSAGE: {type(msg)}]"
                    })

    logger.debug(f"Processed messages result ({len(processed_messages)} messages): {processed_messages}")
    return processed_messages

def count_tokens_openrouter(text, model):
    """Count tokens in text using tiktoken for OpenRouter models"""
    try:
        import tiktoken
        # Extract the base model name from OpenRouter format (e.g., "openai/gpt-4" -> "gpt-4")
        base_model = model.split("/")[-1] if "/" in model else model
        encoding = tiktoken.encoding_for_model(base_model)
        return {
            TOKEN_COUNT_KEYS["PROMPT_TOKENS"]: len(encoding.encode(text)),
            TOKEN_COUNT_KEYS["COMPLETION_TOKENS"]: 0,
            TOKEN_COUNT_KEYS["TOTAL_TOKENS"]: len(encoding.encode(text))
        }
    except Exception as e:
        logger.warning(f"Failed to count tokens for OpenRouter: {e}")
        return DEFAULT_TOKEN_COUNT

def log_openrouter_call(provider, request_args, response, duration, success):
    """Log an OpenRouter API call according to the unified TROPIR schema."""
    try:
        # Prepend "Openrouter - " to the provider name in the response object
        if hasattr(response, 'provider'):
            response.provider = f"Openrouter - {response.provider}"
        elif isinstance(response, dict) and 'provider' in response:
            response['provider'] = f"Openrouter - {response['provider']}"
        elif hasattr(response, 'json') and callable(response.json):
            try:
                response_dict = response.json()
                if isinstance(response_dict, dict) and 'provider' in response_dict:
                    response_dict['provider'] = f"Openrouter - {response_dict['provider']}"
            except Exception:
                pass
                
        # Determine provider for the log entry
        modified_provider = provider
        
        # If we have a provider from the response, use that
        if isinstance(response, dict) and 'provider' in response:
            modified_provider = f"Openrouter - {response['provider']}"
        # Otherwise, just prepend Openrouter to whatever provider was passed in (if not already "openrouter")
        elif provider != "openrouter":
            modified_provider = f"Openrouter - {provider}"

        # Extract messages and model from request_args
        # request_args is a direct dictionary with model and messages
        messages = request_args.get("messages", [])
        model = request_args.get("model", "unknown")
        
        # Log raw messages for debugging
        logger.debug(f"Raw messages before processing: {messages}")
        
        # Process messages to handle various formats and content types
        processed_messages = process_messages(messages)
        
        # This is a sanity check to ensure we're preserving assistant messages
        assistant_messages = [msg for msg in processed_messages if msg.get("role") == "assistant"]
        if assistant_messages:
            logger.debug(f"Found {len(assistant_messages)} assistant messages after processing")
            for idx, msg in enumerate(assistant_messages):
                logger.debug(f"Assistant message {idx}: {msg}")
        
        # We'll log all messages, including assistant and tool messages
        standardized_request = {
            "model": model,
            "messages": processed_messages,
            "temperature": request_args.get("temperature"),
            "max_tokens": request_args.get("max_tokens"),
            "top_p": request_args.get("top_p"),
            "frequency_penalty": request_args.get("frequency_penalty"),
            "presence_penalty": request_args.get("presence_penalty"),
            "stop": request_args.get("stop"),
            "n": request_args.get("n")
        }
        
        # Standardize tools format if present
        if "tools" in request_args:
            standardized_tools = []
            for tool in request_args.get("tools", []):
                if "function" in tool:
                    function = tool["function"]
                    standardized_tool = {
                        "name": function.get("name", ""),
                        "description": function.get("description", ""),
                        "parameters": function.get("parameters", {})
                    }
                    standardized_tools.append(standardized_tool)
            
            if standardized_tools:
                standardized_request["tools"] = standardized_tools
                
        # Add tool_choice if specified
        if "tool_choice" in request_args:
            standardized_request["tool_choice"] = request_args["tool_choice"]
        
        # Extract response text and usage from response
        response_text = ""
        usage = {}
        function_call_info = None
        reasoning = None
        
        # Check for stored JSON data on HTTP response objects
        response_json = None
        if hasattr(response, '_tropir_json_data'):
            response_json = response._tropir_json_data
            logger.debug(f"Found stored JSON data on response object: {bool(response_json)}")
        elif hasattr(response, 'status_code') and hasattr(response, 'json') and callable(response.json):
            try:
                response_json = response.json()
                logger.debug("Retrieved JSON data from response.json() call")
            except Exception as e:
                logger.warning(f"Failed to get JSON from HTTP response: {e}")
        
        # Handle different response types
        try:
            # First check if we have JSON data from HTTP response
            if response_json:
                logger.debug("Processing stored JSON response")
                
                # Extract response text from choices
                if "choices" in response_json and response_json["choices"]:
                    choice = response_json["choices"][0]
                    
                    if "message" in choice:
                        message = choice["message"]
                        
                        # Extract content
                        if "content" in message and message["content"] is not None:
                            response_text = message["content"]
                            
                        # Extract reasoning if present
                        if "reasoning" in message:
                            reasoning = message["reasoning"]
                        
                        # Handle function calls
                        if "function_call" in message and message["function_call"]:
                            func_call = message["function_call"]
                            name = func_call.get("name", "unknown_function")
                            args = func_call.get("arguments", "{}")
                            
                            function_call_info = {
                                "calls": [
                                    {
                                        "id": f"call_{uuid.uuid4().hex[:8]}",
                                        "type": "function",
                                        "function": {
                                            "name": name,
                                            "arguments": args
                                        }
                                    }
                                ]
                            }
                            
                            # Try to parse arguments
                            try:
                                args_obj = json.loads(args)
                                function_call_info["parsed_arguments"] = args_obj
                            except Exception:
                                function_call_info["parsed_arguments"] = {}
                            
                            # Format response text if content was None
                            if not response_text:
                                response_text = f"[FUNCTION_CALL: {name}({args})]"
                        
                        # Handle tool calls
                        elif "tool_calls" in message and message["tool_calls"]:
                            tool_calls = []
                            parsed_args_combined = {}
                            
                            for tool in message["tool_calls"]:
                                tool_details = {
                                    "id": tool.get("id", f"call_{uuid.uuid4().hex[:8]}"),
                                    "type": tool.get("type", "function")
                                }
                                
                                # Handle both nested and flat function structures
                                if "function" in tool:
                                    function = tool["function"]
                                    tool_details["function"] = {
                                        "name": function.get("name", "unknown"),
                                        "arguments": function.get("arguments", "{}")
                                    }
                                    
                                    # Try to parse arguments
                                    try:
                                        args_obj = json.loads(tool_details["function"]["arguments"])
                                        # Store args for the first tool call or the one with most data
                                        if not parsed_args_combined or len(args_obj) > len(parsed_args_combined):
                                            parsed_args_combined = args_obj
                                    except Exception:
                                        pass
                                elif "name" in tool and "arguments" in tool:
                                    # Flatter structure sometimes seen in responses
                                    tool_details["function"] = {
                                        "name": tool.get("name", "unknown"),
                                        "arguments": tool.get("arguments", "{}")
                                    }
                                    
                                    # Try to parse arguments
                                    try:
                                        args_obj = json.loads(tool_details["function"]["arguments"])
                                        if not parsed_args_combined or len(args_obj) > len(parsed_args_combined):
                                            parsed_args_combined = args_obj
                                    except Exception:
                                        pass
                                
                                tool_calls.append(tool_details)
                            
                            if tool_calls:
                                function_call_info = {
                                    "calls": tool_calls,
                                    "parsed_arguments": parsed_args_combined
                                }
                                
                                # If we didn't get any content text, create a placeholder
                                if not response_text:
                                    tool_call_texts = []
                                    for tool in tool_calls:
                                        if "function" in tool:
                                            name = tool["function"].get("name", "unknown")
                                            args = tool["function"].get("arguments", "{}")
                                            tool_call_texts.append(f"[FUNCTION_CALL: {name}({args})]")
                                    response_text = "\n".join(tool_call_texts) if tool_call_texts else "[TOOL_CALLS: Empty]"
                
                # Extract usage information
                if "usage" in response_json:
                    usage = response_json["usage"]
            
            # Try to handle as OpenAI SDK response
            elif hasattr(response, "choices") or hasattr(response, "model_dump") or hasattr(response, "to_dict"):
                # Convert response to dictionary if possible
                if hasattr(response, "model_dump"):
                    response_dict = response.model_dump()
                elif hasattr(response, "to_dict"):
                    response_dict = response.to_dict()
                else:
                    response_dict = vars(response)
                
                logger.debug(f"Response dict: {response_dict}")
                
                # Extract response text from choices
                if "choices" in response_dict and response_dict["choices"]:
                    choice = response_dict["choices"][0]
                    if "message" in choice:
                        message = choice["message"]
                        if "content" in message:
                            response_text = message["content"]
                        
                        # Extract reasoning if present
                        if "reasoning" in message:
                            reasoning = message["reasoning"]
                        
                        # Handle tool calls
                        if "tool_calls" in message and message["tool_calls"]:
                            tool_calls = []
                            parsed_args_combined = {}
                            
                            for tool_call in message["tool_calls"]:
                                if "function" in tool_call:
                                    function = tool_call["function"]
                                    tool_detail = {
                                        "id": tool_call.get("id", str(uuid.uuid4())),
                                        "type": "function",
                                        "function": {
                                            "name": function.get("name", "unknown"),
                                            "arguments": function.get("arguments", "{}")
                                        }
                                    }
                                    tool_calls.append(tool_detail)
                                    
                                    # Try to parse arguments
                                    try:
                                        args_obj = json.loads(tool_detail["function"]["arguments"])
                                        if not parsed_args_combined or len(args_obj) > len(parsed_args_combined):
                                            parsed_args_combined = args_obj
                                    except Exception:
                                        pass
                            
                            if tool_calls:
                                function_call_info = {
                                    "calls": tool_calls,
                                    "parsed_arguments": parsed_args_combined
                                }
                                
                                # If we didn't get any content text, create a placeholder
                                if not response_text:
                                    tool_call_texts = []
                                    for tool in tool_calls:
                                        if "function" in tool:
                                            name = tool["function"].get("name", "unknown")
                                            args = tool["function"].get("arguments", "{}")
                                            tool_call_texts.append(f"[FUNCTION_CALL: {name}({args})]")
                                    response_text = "\n".join(tool_call_texts) if tool_call_texts else "[TOOL_CALLS: Empty]"
                
                # Extract usage information
                if "usage" in response_dict:
                    usage = response_dict["usage"]
            
        except Exception as e:
            logger.error(f"Error processing response: {e}")
            logger.error(f"Response type: {type(response)}")
            logger.error(f"Response dir: {dir(response)}")
            logger.error(f"Response repr: {repr(response)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            response_text = f"[ERROR_PROCESSING_RESPONSE: {str(e)}]"
        
        # Count tokens if not provided
        if not usage:
            prompt_text = " ".join(str(msg.get("content", "")) for msg in processed_messages if msg.get("content"))
            resp_text_str = str(response_text) if response_text else ""
            usage = count_tokens_openrouter(prompt_text + resp_text_str, standardized_request["model"])
        
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

        # Only try to get details if they exist
        if usage and isinstance(usage, dict):
            # Get prompt details
            prompt_details = usage.get("prompt_tokens_details", {}) or {}
            if isinstance(prompt_details, dict):
                standardized_usage["token_details"]["cached_tokens"] = prompt_details.get("cached_tokens")
                standardized_usage["token_details"]["audio_tokens"] = prompt_details.get("audio_tokens")
            
            # Get completion details
            completion_details = usage.get("completion_tokens_details", {}) or {}
            if isinstance(completion_details, dict):
                # Get reasoning tokens
                standardized_usage["token_details"]["reasoning_tokens"] = completion_details.get("reasoning_tokens")
                
                # Get prediction tokens
                standardized_usage["token_details"]["accepted_prediction_tokens"] = completion_details.get("accepted_prediction_tokens")
                standardized_usage["token_details"]["rejected_prediction_tokens"] = completion_details.get("rejected_prediction_tokens")
                
                # Add any audio tokens from completion details
                if completion_details.get("audio_tokens") is not None:
                    if standardized_usage["token_details"]["audio_tokens"] is None:
                        standardized_usage["token_details"]["audio_tokens"] = 0
                    standardized_usage["token_details"]["audio_tokens"] += completion_details["audio_tokens"]

        # Generate log entry with standardized request
        log_entry = create_base_log_entry(modified_provider, standardized_request)
        
        # Final verification of messages before logging
        if "request" in log_entry and "messages" in log_entry["request"]:
            logger.debug(f"Messages in final log entry: {len(log_entry['request']['messages'])}")
            # Check for assistant messages in the final log entry
            assistant_msgs = [msg for msg in log_entry["request"]["messages"] if msg.get("role") == "assistant"]
            if assistant_msgs:
                logger.debug(f"Assistant messages in final log entry: {len(assistant_msgs)}")
            else:
                logger.warning("No assistant messages found in final log entry")
        
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
        
        # Add tool_calls field if we have function call information
        if function_call_info:
            log_entry["tool_calls"] = function_call_info
        
        # Remove any leftover function_call field if it exists (to be consistent with schema)
        if "function_call" in log_entry:
            del log_entry["function_call"]
        
        # Write to log file
        send_log(log_entry)
        logger.debug(f"Successfully logged OpenRouter call for model: {standardized_request['model']}")

    except Exception as e:
        logger.error(f"Error logging OpenRouter call: {str(e)}")
        logger.error(traceback.format_exc())

def patched_requests_post(original_post, *args, **kwargs):
    """
    Patched version of requests.post to track direct HTTP calls to OpenRouter API.
    """
    url = args[0] if args else kwargs.get('url')
    
    # Only process OpenRouter API calls
    if url and isinstance(url, str) and "openrouter.ai/api" in url:
        try:
            start_time = time.time()
            success = True
            
            # Get the request data
            request_data = {}
            if 'json' in kwargs:
                # First check if there's a json parameter (preferred by requests)
                request_data = kwargs['json']
                logger.debug(f"Original JSON request data to OpenRouter: {request_data}")
            elif 'data' in kwargs:
                # Fall back to data parameter
                try:
                    data = kwargs['data']
                    if isinstance(data, str):
                        request_data = json.loads(data)
                        logger.debug(f"Original data request data to OpenRouter: {request_data}")
                    else:
                        request_data = {'data': data}
                except (json.JSONDecodeError, TypeError):
                    request_data = {'data': kwargs['data']}
            
            # Make the actual request
            try:
                response = original_post(*args, **kwargs)
                
                # Store the JSON response for later processing
                try:
                    response_data = response.json()
                    response._tropir_json_data = response_data
                    success = response.status_code < 400
                except Exception as json_error:
                    logger.error(f"Failed to parse JSON from OpenRouter response: {json_error}")
                    success = False
            except Exception as e:
                success = False
                response = None
                logger.error(f"Error making OpenRouter HTTP request: {str(e)}")
                raise e
            finally:
                duration = time.time() - start_time
                
                # Only log if this is a chat completion or similar endpoint
                if "chat/completions" in url or "completions" in url:
                    # Special handling for messages to ensure assistant messages with tool calls are preserved
                    if 'messages' in request_data:
                        messages = request_data['messages']
                        assistant_messages = [msg for msg in messages if msg.get('role') == 'assistant']
                        logger.debug(f"Assistant messages in request: {assistant_messages}")
                    
                    # Log the API call
                    logger.debug(f"Logging direct OpenRouter API call to {url}")
                    log_openrouter_call("openrouter", request_data, response, duration, success)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in patched requests.post: {str(e)}")
            logger.error(traceback.format_exc())
            # Let the original request proceed even if tracking fails
            return original_post(*args, **kwargs)
    else:
        # For non-OpenRouter URLs, just call the original function
        return original_post(*args, **kwargs)

async def patched_httpx_async_post(original_post, self, url, *args, **kwargs):
    """
    Patched version of httpx.AsyncClient.post to track direct HTTP calls to OpenRouter API.
    """
    # Only process OpenRouter API calls
    if url and isinstance(url, str) and "openrouter.ai/api" in url:
        try:
            start_time = time.time()
            success = True
            
            # Get the request data
            request_data = {}
            if 'json' in kwargs:
                # First check if there's a json parameter (preferred by requests)
                request_data = kwargs['json']
                logger.debug(f"Original JSON request data to OpenRouter: {request_data}")
            elif 'data' in kwargs:
                # Fall back to data parameter
                try:
                    data = kwargs['data']
                    if isinstance(data, str):
                        request_data = json.loads(data)
                        logger.debug(f"Original data request data to OpenRouter: {request_data}")
                    else:
                        request_data = {'data': data}
                except (json.JSONDecodeError, TypeError):
                    request_data = {'data': kwargs['data']}
            
            # Make the actual request
            try:
                response = await original_post(self, url, *args, **kwargs)
                
                # Store the JSON response for later processing
                try:
                    response_data = response.json()
                    response._tropir_json_data = response_data
                    success = response.status_code < 400
                except Exception as json_error:
                    logger.error(f"Failed to parse JSON from OpenRouter response: {json_error}")
                    success = False
            except Exception as e:
                success = False
                response = None
                logger.error(f"Error making OpenRouter HTTP request: {str(e)}")
                raise e
            finally:
                duration = time.time() - start_time
                
                # Only log if this is a chat completion or similar endpoint
                if "chat/completions" in url or "completions" in url:
                    # Special handling for messages to ensure assistant messages with tool calls are preserved
                    if 'messages' in request_data:
                        messages = request_data['messages']
                        assistant_messages = [msg for msg in messages if msg.get('role') == 'assistant']
                        logger.debug(f"Assistant messages in request: {assistant_messages}")
                    
                    # Add URL to request data for proper logging
                    if isinstance(request_data, dict):
                        request_data["url"] = url
                    
                    # Log the API call
                    logger.debug(f"Logging direct OpenRouter API call to {url}")
                    log_openrouter_call("openrouter", request_data, response, duration, success)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in patched httpx.AsyncClient.post: {str(e)}")
            logger.error(traceback.format_exc())
            # Let the original request proceed even if tracking fails
            return await original_post(self, url, *args, **kwargs)
    else:
        # For non-OpenRouter URLs, just call the original function
        return await original_post(self, url, *args, **kwargs)

def patch_openai_client_init():
    """Patch the OpenAI client initialization to detect OpenRouter base URLs"""
    try:
        from openai import OpenAI
        
        # Store the original __init__ method
        original_init = OpenAI.__init__
        
        @functools.wraps(original_init)
        def patched_init(self, *args, **kwargs):
            # Call the original __init__
            original_init(self, *args, **kwargs)
            
            # Check if this client is configured for OpenRouter
            base_url = None
            
            # Check kwargs first
            if "base_url" in kwargs:
                base_url = kwargs["base_url"]
            # Then check args (positional arguments)
            elif len(args) >= 1 and isinstance(args[0], dict) and "base_url" in args[0]:
                base_url = args[0]["base_url"]
            # Finally check if it's set as an attribute
            elif hasattr(self, "base_url"):
                base_url = self.base_url
                
            if base_url and is_openrouter_url(base_url):
                # Mark this client as an OpenRouter client
                logger.debug(f"OpenAI client initialized with OpenRouter base_url: {base_url}")
                setattr(self, "_is_openrouter_client", True)
        
        # Apply the patch
        OpenAI.__init__ = patched_init
        logger.info("Successfully patched OpenAI client initialization for OpenRouter detection")
    
    except ImportError:
        logger.warning("Could not import OpenAI. Client initialization patching skipped.")
    except Exception as e:
        logger.error(f"Failed to patch OpenAI client initialization: {e}")
        logger.error(traceback.format_exc())

def setup_openrouter_patching():
    """Set up tracking for OpenRouter by patching target methods."""
    try:
        # Patch requests.post for direct API calls
        if not getattr(requests.post, '_openrouter_patched', False):
            original_post = requests.post
            patched_post = functools.wraps(original_post)(
                lambda *args, **kwargs: patched_requests_post(original_post, *args, **kwargs)
            )
            patched_post._openrouter_patched = True
            requests.post = patched_post
            logger.info("Successfully patched requests.post for OpenRouter API tracking")

        # Patch httpx.AsyncClient.post for async API calls
        try:
            import httpx
            if not getattr(httpx.AsyncClient.post, '_openrouter_patched', False):
                logger.info("Patching httpx.AsyncClient.post for direct OpenRouter API calls")
                original_async_post = httpx.AsyncClient.post
                
                # Create an async wrapper that maintains the function signature
                @functools.wraps(original_async_post)
                async def async_wrapper(self, url, *args, **kwargs):
                    return await patched_httpx_async_post(original_async_post, self, url, *args, **kwargs)
                
                # Mark as patched with a specific tag for HTTP patching
                async_wrapper._openrouter_patched = True
                httpx.AsyncClient.post = async_wrapper
                logger.info("Successfully patched httpx.AsyncClient.post for direct OpenRouter API calls")
            else:
                logger.info("httpx.AsyncClient.post already patched for direct OpenRouter API calls")
        except ImportError:
            logger.debug("Could not import 'httpx'. Direct HTTP patching for httpx will be skipped.")

        # Patch the OpenAI client initialization
        patch_openai_client_init()
            
        # Import the specific class where the 'create' method resides
        from openai.resources.chat.completions import Completions as OpenAICompletions

        # Check if the 'create' method exists and hasn't been patched yet
        if hasattr(OpenAICompletions, "create") and not getattr(OpenAICompletions.create, '_openrouter_patched', False):
            original_create_method = OpenAICompletions.create  # Get the original function

            # Create a wrapper that checks if this is an OpenRouter request
            @functools.wraps(original_create_method)
            def patched_create_method(self, *args, **kwargs):
                # Check if the client is configured for OpenRouter
                base_url = getattr(self._client, "base_url", None)
                client_is_openrouter = getattr(self._client, "_is_openrouter_client", False) or is_openrouter_url(base_url)
                
                # Check for OpenRouter model format
                model_is_openrouter = False
                if "model" in kwargs and is_openrouter_model_format(kwargs["model"]):
                    model_is_openrouter = True
                
                # If this looks like an OpenRouter call, track it as such
                if client_is_openrouter or model_is_openrouter:
                    # Log the original request with all message types
                    if "messages" in kwargs:
                        logger.debug(f"OpenRouter SDK call messages: {kwargs['messages']}")
                        # Extract assistant messages for debug
                        assistant_messages = [msg for msg in kwargs['messages'] 
                                             if (isinstance(msg, dict) and msg.get('role') == 'assistant') or 
                                             (hasattr(msg, 'role') and msg.role == 'assistant')]
                        if assistant_messages:
                            logger.debug(f"Found {len(assistant_messages)} assistant messages in request")
                            for idx, msg in enumerate(assistant_messages):
                                if isinstance(msg, dict):
                                    logger.debug(f"Assistant message {idx}: {msg}")
                                else:
                                    logger.debug(f"Assistant message {idx} (object): role={msg.role}, has_tool_calls={hasattr(msg, 'tool_calls')}")
                        
                    start_time = time.time()
                    success = True
                    try:
                        response = original_create_method(self, *args, **kwargs)
                    except Exception as e:
                        success = False
                        response = None
                        logger.error(f"Error in OpenRouter call: {str(e)}")
                        raise e
                    finally:
                        duration = time.time() - start_time
                        logger.debug(f"Logging OpenRouter call via OpenAI SDK - model: {kwargs.get('model', 'unknown')}, base_url: {base_url}")
                        # Make a deep copy of kwargs to avoid modifying the original
                        request_args = {}
                        for key, value in kwargs.items():
                            # Special handling for messages to preserve all message types
                            if key == "messages":
                                # Create a deep copy of messages
                                if isinstance(value, list):
                                    request_args[key] = list(value)  # Shallow copy the list
                                else:
                                    request_args[key] = value
                            else:
                                request_args[key] = value
                                
                        # Debug the messages in request_args before logging
                        if "messages" in request_args:
                            assistant_msgs = [msg for msg in request_args["messages"] 
                                             if (isinstance(msg, dict) and msg.get('role') == 'assistant') or 
                                             (hasattr(msg, 'role') and msg.role == 'assistant')]
                            if assistant_msgs:
                                logger.debug(f"Assistant messages in request_args before logging: {len(assistant_msgs)}")
                            else:
                                logger.warning("No assistant messages found in request_args before logging")
                                
                        log_openrouter_call("openrouter", request_args, response, duration, success)
                    return response
                
                # For non-OpenRouter requests, let the original method handle it
                return original_create_method(self, *args, **kwargs)

            # Replace the original method with the patched one
            OpenAICompletions.create = patched_create_method
            OpenAICompletions.create._openrouter_patched = True
            logger.info("Successfully patched OpenAI Completions.create for OpenRouter tracking")

        # Patch the responses methods
        try:
            from openai.resources.responses import Responses as OpenAIResponses
            
            # Patch synchronous Responses methods
            methods_to_patch = ['create', 'stream', 'parse', 'retrieve', 'delete']
            
            for method_name in methods_to_patch:
                if hasattr(OpenAIResponses, method_name) and not getattr(getattr(OpenAIResponses, method_name), '_openrouter_patched', False):
                    original_method = getattr(OpenAIResponses, method_name)
                    
                    # Create patched version that handles OpenRouter requests
                    @functools.wraps(original_method)
                    def patched_method(self, *args, **kwargs):
                        # Check if the client is configured for OpenRouter
                        base_url = getattr(self._client, "base_url", None)
                        client_is_openrouter = getattr(self._client, "_is_openrouter_client", False) or is_openrouter_url(base_url)
                        
                        # Check for OpenRouter model format
                        model_is_openrouter = False
                        if "model" in kwargs and is_openrouter_model_format(kwargs["model"]):
                            model_is_openrouter = True
                        
                        # If this looks like an OpenRouter call, track it as such
                        if client_is_openrouter or model_is_openrouter:
                            # Log the original request with all message types
                            if "messages" in kwargs:
                                logger.debug(f"OpenRouter SDK {method_name} call messages: {kwargs['messages']}")
                                # Extract assistant messages for debug
                                assistant_messages = [msg for msg in kwargs['messages'] 
                                                     if (isinstance(msg, dict) and msg.get('role') == 'assistant') or 
                                                     (hasattr(msg, 'role') and msg.role == 'assistant')]
                                if assistant_messages:
                                    logger.debug(f"Found {len(assistant_messages)} assistant messages in {method_name} request")
                                
                            start_time = time.time()
                            success = True
                            try:
                                response = original_method(self, *args, **kwargs)
                            except Exception as e:
                                success = False
                                response = None
                                logger.error(f"Error in OpenRouter {method_name} call: {str(e)}")
                                raise e
                            finally:
                                duration = time.time() - start_time
                                logger.debug(f"Logging OpenRouter {method_name} call via OpenAI SDK")
                                # Make a deep copy of kwargs to avoid modifying the original
                                request_args = {}
                                for key, value in kwargs.items():
                                    # Special handling for messages to preserve all message types
                                    if key == "messages":
                                        # Create a deep copy of messages
                                        if isinstance(value, list):
                                            request_args[key] = list(value)  # Shallow copy the list
                                        else:
                                            request_args[key] = value
                                    else:
                                        request_args[key] = value
                                        
                                log_openrouter_call("openrouter", request_args, response, duration, success)
                            return response
                        
                        # For non-OpenRouter requests, let the original method handle it
                        return original_method(self, *args, **kwargs)
                    
                    # Set the method with the patched version
                    setattr(OpenAIResponses, method_name, patched_method)
                    getattr(OpenAIResponses, method_name)._openrouter_patched = True
            
            logger.info("Successfully patched OpenAI Responses methods for OpenRouter tracking")
                    
        except ImportError:
            logger.warning("Could not import OpenAI responses classes. OpenRouter responses tracking may not work.")
        except Exception as e:
            logger.error(f"Failed during OpenRouter responses patching: {e}")
            logger.error(traceback.format_exc())

    except ImportError:
        logger.warning("Could not import 'openai.resources.chat.completions.Completions'. OpenRouter tracking may not work.")
    except Exception as e:
        logger.error(f"Failed during OpenRouter patching process: {e}")
        logger.error(traceback.format_exc()) 