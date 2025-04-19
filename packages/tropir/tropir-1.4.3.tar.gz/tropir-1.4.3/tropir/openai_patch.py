"""
OpenAI-specific patching logic for LLM tracking.
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
#   
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
from .openrouter_patch import is_openrouter_url

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

def process_messages(messages):
    """Process OpenAI messages to handle special content types"""
    processed_messages = []
    
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
            result.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "").strip('\n') if isinstance(msg.get("content"), str) else msg.get("content")
            })
        return result
    
    # Original processing logic for standard messages format
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

            processed_messages.append(processed_msg)
        else:
            # Handle non-dict message objects
            try:
                # For OpenAI message objects
                content = getattr(msg, "content", str(msg))
                if isinstance(content, str):
                    content = content.strip('\n')
                
                processed_msg = {
                    "role": getattr(msg, "role", "unknown"),
                    "content": content
                }
                
                # Add tool calls if present
                if getattr(msg, "tool_calls", None):
                    if hasattr(msg.tool_calls, "model_dump"):
                        processed_msg["tool_calls"] = [t.model_dump() for t in msg.tool_calls]
                    else:
                        # Try to extract tool calls as dictionaries
                        tool_calls = []
                        for t in msg.tool_calls:
                            if hasattr(t, "__dict__"):
                                tool_calls.append(vars(t))
                            else:
                                tool_calls.append(str(t))
                        processed_msg["tool_calls"] = tool_calls
                
                # Add tool call ID if present (for tool results)
                if getattr(msg, "tool_call_id", None):
                    processed_msg["tool_call_id"] = msg.tool_call_id
                
                # Add name if present (for functions/tools)
                if getattr(msg, "name", None):
                    processed_msg["name"] = msg.name
                
                processed_messages.append(processed_msg)
            except Exception as e:
                # If all else fails, create a basic message
                logger.warning(f"Error processing message object: {e}")
                processed_messages.append({
                    "role": getattr(msg, "role", "unknown"),
                    "content": str(getattr(msg, "content", str(msg)))
                })

    return processed_messages

def count_tokens_openai(text, model):
    """Count tokens in text using tiktoken for OpenAI models"""
    try:
        import tiktoken
        encoding = tiktoken.encoding_for_model(model)
        return {
            TOKEN_COUNT_KEYS["PROMPT_TOKENS"]: len(encoding.encode(text)),
            TOKEN_COUNT_KEYS["COMPLETION_TOKENS"]: 0,
            TOKEN_COUNT_KEYS["TOTAL_TOKENS"]: len(encoding.encode(text))
        }
    except Exception as e:
        logger.warning(f"Failed to count tokens for OpenAI: {e}")
        return DEFAULT_TOKEN_COUNT

def log_openai_call(provider, request_args, response, duration, success):
    """Log an OpenAI API call according to the unified TROPIR schema."""
    try:
        # Skip if this appears to be an OpenRouter request
        if "model" in request_args and isinstance(request_args["model"], str) and "/" in request_args["model"]:
            model_parts = request_args["model"].split("/")
            if len(model_parts) >= 2 and model_parts[0] in ["openai", "anthropic", "google", "meta", "cohere"]:
                logger.debug(f"Skipping OpenAI logging for OpenRouter request with model: {request_args['model']}")
                return

        # Extract messages from request_args, handling responses.create format
        messages = []
        if "messages" in request_args:
            # Standard chat.completions.create format
            messages = request_args.get("messages", [])
        elif "input" in request_args:
            # responses.create format
            if isinstance(request_args["input"], str):
                input_data = request_args["input"]
                instructions = request_args.get("instructions", "")
                
                if instructions:
                    messages = [
                        {"role": "system", "content": instructions},
                        {"role": "user", "content": input_data}
                    ]
                else:
                    messages = [{"role": "user", "content": input_data}]
            elif isinstance(request_args["input"], list):
                # Handle list of role/content pairs
                messages = request_args["input"]
        
        processed_messages = process_messages(messages)
        
        # Create standardized request structure
        standardized_request = {
            "model": request_args.get("model", "unknown"),
            "messages": processed_messages,
            "temperature": request_args.get("temperature"),
            "max_tokens": request_args.get("max_tokens"),
            "top_p": request_args.get("top_p"),
            "frequency_penalty": request_args.get("frequency_penalty"),
            "presence_penalty": request_args.get("presence_penalty"),
            "stop": request_args.get("stop"),
            "n": request_args.get("n")
        }
        
        # Store response_format if it exists for structured output info
        structured_output_info = None
        if "response_format" in request_args:
            structured_output_info = request_args.get("response_format")
            standardized_request["response_format"] = structured_output_info
        
        # Standardize tools format from functions or tools
        tools = []
        
        # Check if this is a function/tool call request
        if "functions" in request_args:
            for func in request_args.get("functions", []):
                standardized_tool = {
                    "name": func.get("name", ""),
                    "description": func.get("description", ""),
                    "parameters": func.get("parameters", {})
                }
                tools.append(standardized_tool)
                
            # Add tool_choice if function_call was specified
            if "function_call" in request_args:
                if isinstance(request_args["function_call"], dict):
                    standardized_request["tool_choice"] = {
                        "type": "function",
                        "function": {
                            "name": request_args["function_call"].get("name", "auto")
                        }
                    }
                else:
                    standardized_request["tool_choice"] = request_args["function_call"]
                    
        # Process tools field if it exists
        elif "tools" in request_args:
            tools = request_args.get("tools", [])
            if "tool_choice" in request_args:
                standardized_request["tool_choice"] = request_args["tool_choice"]
                
        # Add tools to request if we have any
        if tools:
            standardized_request["tools"] = tools
        
        response_text = ""
        usage = {}
        function_call_info = None
        model = standardized_request.get("model", "unknown")
        
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
            # Extract response text from choices
            if "choices" in response_json and response_json["choices"]:
                choice = response_json["choices"][0]
                
                if "message" in choice:
                    message = choice["message"]
                    
                    # Extract content
                    if "content" in message and message["content"] is not None:
                        response_text = message["content"]
                    
                    # Extract function call
                    if "function_call" in message and message["function_call"]:
                        func_call = message["function_call"]
                        name = func_call.get("name", "unknown_function")
                        args = func_call.get("arguments", "{}")
                        
                        # Store function call info in tool_calls format
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
                    
                    # Extract tool calls
                    elif "tool_calls" in message and message["tool_calls"]:
                        tool_calls = message["tool_calls"]
                        tool_call_details = []
                        parsed_args_combined = {}
                        
                        for tool in tool_calls:
                            tool_details = {
                                "id": tool.get("id", f"call_{uuid.uuid4().hex[:8]}"),
                                "type": tool.get("type", "function"),
                                "function": {
                                    "name": tool.get("function", {}).get("name", "unknown_function"),
                                    "arguments": tool.get("function", {}).get("arguments", "{}")
                                }
                            }
                            
                            # Try to parse arguments
                            try:
                                args_obj = json.loads(tool_details["function"]["arguments"])
                                # Store args for the first tool call or the one with most data
                                if not parsed_args_combined or len(args_obj) > len(parsed_args_combined):
                                    parsed_args_combined = args_obj
                            except Exception:
                                pass
                                
                            tool_call_details.append(tool_details)
                        
                        # Store all tool calls
                        function_call_info = {
                            "calls": tool_call_details,
                            "parsed_arguments": parsed_args_combined
                        }
                        
                        # Format response text if content was None
                        if not response_text:
                            response_text = f"[TOOL_CALLS: {len(message['tool_calls'])}]"
                
                # Extract delta for streaming responses
                elif "delta" in choice:
                    delta = choice["delta"]
                    if "content" in delta and delta["content"] is not None:
                        response_text = delta["content"]
                    elif "function_call" in delta or "tool_calls" in delta:
                        response_text = "[STREAMING_FUNCTION_CALL]"
                    else:
                        response_text = "[STREAMING_RESPONSE]"
            
            # Extract usage information
            if "usage" in response_json:
                usage = response_json["usage"]
        
        # Handle responses.create format response
        elif hasattr(response, "output_text") or hasattr(response, "text"):
            # responses.create format uses output_text or text
            response_text = getattr(response, "output_text", None) or getattr(response, "text", "")
            
            # Extract usage if available
            if hasattr(response, "usage"):
                if hasattr(response.usage, "model_dump"):
                    usage = response.usage.model_dump()
                else:
                    try:
                        usage = vars(response.usage)
                    except:
                        usage = {}
            
            # Handle streaming in_progress attribute
            if hasattr(response, "in_progress") and response.in_progress:
                if not response_text:
                    response_text = "[STREAMING_RESPONSE]"
        
        # Handle OpenAI responses
        elif hasattr(response, "to_dict"):
            # Dictionary approach
            response_dict = response.to_dict()
            
            # Extract response text from choices
            if "choices" in response_dict and response_dict["choices"]:
                choice = response_dict["choices"][0]
                
                if "message" in choice and choice["message"]:
                    message = choice["message"]
                    
                    # Check for content
                    if "content" in message and message["content"] is not None:
                        response_text = message["content"]
                    
                    # Check for parsed structured output
                    if "parsed" in message and message["parsed"] is not None:
                        if not structured_output_info:
                            structured_output_info = {"parsed": message["parsed"]}
                    
                    # Check for function call
                    if "function_call" in message and message["function_call"]:
                        func_call = message["function_call"]
                        name = func_call.get("name", "unknown_function")
                        args = func_call.get("arguments", "{}")
                        
                        # Store function call info in tool_calls format
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
                    
                    # Check for tool calls
                    elif "tool_calls" in message and message["tool_calls"]:
                        tool_calls = message["tool_calls"]
                        tool_call_details = []
                        parsed_args_combined = {}
                        
                        for tool in tool_calls:
                            tool_details = {
                                "id": tool.get("id", f"call_{uuid.uuid4().hex[:8]}"),
                                "type": tool.get("type", "function"),
                                "function": {
                                    "name": tool.get("function", {}).get("name", "unknown_function"),
                                    "arguments": tool.get("function", {}).get("arguments", "{}")
                                }
                            }
                            
                            # Try to parse arguments
                            try:
                                args_obj = json.loads(tool_details["function"]["arguments"])
                                # Store args for the first tool call or the one with most data
                                if not parsed_args_combined or len(args_obj) > len(parsed_args_combined):
                                    parsed_args_combined = args_obj
                            except Exception:
                                pass
                                
                            tool_call_details.append(tool_details)
                        
                        # Store all tool calls
                        function_call_info = {
                            "calls": tool_call_details,
                            "parsed_arguments": parsed_args_combined
                        }
                        
                        # Format response text if content was None
                        if not response_text:
                            response_text = f"[TOOL_CALLS: {len(message['tool_calls'])}]"
                
                elif "delta" in choice and choice["delta"]:
                    # Streaming response
                    if "content" in choice["delta"] and choice["delta"]["content"]:
                        response_text = choice["delta"]["content"]
                    else:
                        response_text = "[STREAMING_RESPONSE]"
            
            # Extract usage information
            if "usage" in response_dict:
                usage = response_dict["usage"]
        
        # Attribute-based approach if dictionary approach failed
        if not response_text and hasattr(response, "choices") and response.choices:
            if hasattr(response.choices[0], "message") and response.choices[0].message:
                message = response.choices[0].message
                
                # Check content
                if hasattr(message, "content") and message.content is not None:
                    response_text = message.content
                
                # Check parsed structured output
                if hasattr(message, "parsed") and message.parsed is not None:
                    if not structured_output_info:
                        # Try to get the parsed data
                        try:
                            parsed_data = message.parsed
                            if hasattr(parsed_data, "model_dump"):
                                structured_output_info = {"parsed": parsed_data.model_dump()}
                            else:
                                structured_output_info = {"parsed": vars(parsed_data)}
                        except Exception:
                            structured_output_info = {"parsed": str(message.parsed)}
                
                # Check function call
                if hasattr(message, "function_call") and message.function_call:
                    try:
                        func_call = message.function_call
                        name = getattr(func_call, "name", "unknown_function")
                        args = getattr(func_call, "arguments", "{}")
                        
                        # Store function call info in tool_calls format
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
                            if isinstance(args, str):
                                args_obj = json.loads(args)
                                function_call_info["parsed_arguments"] = args_obj
                            else:
                                function_call_info["parsed_arguments"] = {}
                        except Exception:
                            function_call_info["parsed_arguments"] = {}
                        
                        # Format response text if content was None
                        if not response_text:
                            response_text = f"[FUNCTION_CALL: {name}({args})]"
                    except Exception as e:
                        logger.error(f"Error extracting function call: {e}")
                
                # Check tool calls
                elif hasattr(message, "tool_calls") and message.tool_calls:
                    try:
                        tool_calls = message.tool_calls
                        tool_call_details = []
                        parsed_args_combined = {}
                        
                        for tool in tool_calls:
                            tool_details = {
                                "id": getattr(tool, "id", f"call_{uuid.uuid4().hex[:8]}"),
                                "type": getattr(tool, "type", "function"),
                            }
                            
                            if hasattr(tool, "function"):
                                func = tool.function
                                tool_details["function"] = {
                                    "name": getattr(func, "name", "unknown_function"),
                                    "arguments": getattr(func, "arguments", "{}")
                                }
                                
                                # Try to parse arguments
                                try:
                                    if isinstance(tool_details["function"]["arguments"], str):
                                        args_obj = json.loads(tool_details["function"]["arguments"])
                                        # Store args for the first tool call or the one with most data
                                        if not parsed_args_combined or len(args_obj) > len(parsed_args_combined):
                                            parsed_args_combined = args_obj
                                except Exception:
                                    pass
                            
                            tool_call_details.append(tool_details)
                        
                        # Store all tool calls in standardized format
                        function_call_info = {
                            "calls": tool_call_details,
                            "parsed_arguments": parsed_args_combined
                        }
                        
                        # Format response text if content was None
                        if not response_text:
                            response_text = f"[TOOL_CALLS: {len(tool_calls)}]"
                    except Exception as e:
                        logger.error(f"Error extracting tool calls: {e}")
            
            # Check for streaming response
            elif hasattr(response.choices[0], "delta") and response.choices[0].delta:
                if hasattr(response.choices[0].delta, "content") and response.choices[0].delta.content is not None:
                    response_text = response.choices[0].delta.content
                else:
                    response_text = "[STREAMING_RESPONSE]"

        # Extract usage if available
        if not usage and hasattr(response, "usage"):
            if hasattr(response.usage, "model_dump"):
                usage = response.usage.model_dump()
            else:
                try:
                    usage = vars(response.usage)
                except:
                    usage = {}
                    
        # Count tokens if not provided
        if not usage:
            prompt_text = " ".join(str(msg.get("content", "")) for msg in processed_messages if msg.get("content"))
            resp_text_str = str(response_text) if response_text else ""
            usage = count_tokens_openai(prompt_text + resp_text_str, model)
        
        # Standardize the usage structure with token_details
        standardized_usage = {
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
            "token_details": {
                "cached_tokens": usage.get("prompt_tokens_details", {}).get("cached_tokens", None),
                "audio_tokens": (
                    usage.get("prompt_tokens_details", {}).get("audio_tokens", 0) + 
                    usage.get("completion_tokens_details", {}).get("audio_tokens", 0)
                ) or None,
                "reasoning_tokens": usage.get("completion_tokens_details", {}).get("reasoning_tokens", None),
                "accepted_prediction_tokens": usage.get("completion_tokens_details", {}).get("accepted_prediction_tokens", None),
                "rejected_prediction_tokens": usage.get("completion_tokens_details", {}).get("rejected_prediction_tokens", None)
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
        
        # Add structured_output_info if it exists
        if structured_output_info:
            log_entry["structured_output_info"] = structured_output_info
        
        # Add tool_calls field if we have function call information
        if function_call_info:
            log_entry["tool_calls"] = function_call_info
        
        # Remove any existing function_call field to adhere to schema
        if "function_call" in log_entry:
            del log_entry["function_call"]
        
        # Remove functions_info field from request if it exists
        if "functions_info" in log_entry["request"]:
            del log_entry["request"]["functions_info"]
        
        # Write to log file
        send_log(log_entry)

    except Exception as e:
        logger.error(f"Error logging OpenAI call: {str(e)}")
        logger.error(traceback.format_exc())

def patched_requests_post(original_post, *args, **kwargs):
    """
    Patched version of requests.post to track direct HTTP calls to OpenAI API.
    """
    url = args[0] if args else kwargs.get('url')
    
    # Skip OpenRouter URLs, those are handled by the OpenRouter patch
    if is_openrouter_url(url):
        logger.debug(f"OpenAI patching skipping OpenRouter URL: {url}")
        return original_post(*args, **kwargs)
    
    # Only process specific OpenAI API endpoints to avoid interfering with SDK
    is_openai_api = (
        url and 
        isinstance(url, str) and 
        (
            # Match any OpenAI API endpoints to ensure we catch everything
            "api.openai.com" in url
        )
    )
    
    if is_openai_api:
        try:
            logger.debug(f"Intercepted direct API call to OpenAI endpoint: {url}")
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
            
            # Skip if this looks like an OpenRouter request
            if "model" in request_data and isinstance(request_data["model"], str) and "/" in request_data["model"]:
                model_parts = request_data["model"].split("/")
                if len(model_parts) >= 2 and model_parts[0] in ["openai", "anthropic", "google", "meta", "cohere"]:
                    logger.debug(f"Skipping OpenAI HTTP patching for OpenRouter request with model: {request_data['model']}")
                    return original_post(*args, **kwargs)
            
            # Make the actual request
            try:
                response = original_post(*args, **kwargs)
                
                # Extract JSON data from the response before passing to log function
                try:
                    response_data = response.json()
                    success = response.status_code < 400
                    
                    # Save the response for logging
                    response._tropir_json_data = response_data
                except Exception as json_error:
                    logger.error(f"Failed to parse JSON from OpenAI response: {json_error}")
                    response_data = {"error": {"message": f"Failed to parse response: {str(json_error)}"}}
                    success = False
            except Exception as e:
                success = False
                response = None
                logger.error(f"Error making OpenAI HTTP request: {str(e)}")
                raise
            finally:
                duration = time.time() - start_time
                
                # Only log if this wasn't already logged by the SDK
                if not getattr(request_data, '_tropir_logged', False):
                    logger.info(f"Logging direct OpenAI API call to: {url}")
                    
                    # Log the detailed response
                    log_openai_call("openai", request_data, response, duration, success)
                    
                    # Mark as logged to prevent double-logging
                    if isinstance(request_data, dict):
                        request_data['_tropir_logged'] = True
            
            return response
        except Exception as e:
            logger.error(f"Error in patched requests.post for OpenAI: {str(e)}")
            logger.error(traceback.format_exc())
            # Always let the original request proceed even if tracking fails
            return original_post(*args, **kwargs)
    else:
        # For non-OpenAI URLs, just call the original function
        return original_post(*args, **kwargs)

async def patched_httpx_async_post(original_post, self, url, *args, **kwargs):
    """
    Patched version of httpx.AsyncClient.post to track direct HTTP calls to OpenAI API.
    """
    # Skip OpenRouter URLs, those are handled by the OpenRouter patch
    if is_openrouter_url(url):
        logger.debug(f"OpenAI patching skipping OpenRouter URL: {url}")
        return await original_post(self, url, *args, **kwargs)
    
    # Only process specific OpenAI API endpoints to avoid interfering with SDK
    is_openai_api = (
        url and 
        isinstance(url, str) and 
        (
            # Match any OpenAI API endpoints to ensure we catch everything
            "api.openai.com" in url
        )
    )
    
    if is_openai_api:
        try:
            logger.debug(f"Intercepted direct API call to OpenAI endpoint: {url}")
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
            
            # Skip if this looks like an OpenRouter request
            if "model" in request_data and isinstance(request_data["model"], str) and "/" in request_data["model"]:
                model_parts = request_data["model"].split("/")
                if len(model_parts) >= 2 and model_parts[0] in ["openai", "anthropic", "google", "meta", "cohere"]:
                    logger.debug(f"Skipping OpenAI HTTP patching for OpenRouter request with model: {request_data['model']}")
                    return await original_post(self, url, *args, **kwargs)
            
            # Make the actual request
            try:
                response = await original_post(self, url, *args, **kwargs)
                
                # Extract JSON data from the response before passing to log function
                try:
                    response_data = response.json()
                    success = response.status_code < 400
                    
                    # Save the response for logging
                    response._tropir_json_data = response_data
                except Exception as json_error:
                    logger.error(f"Failed to parse JSON from OpenAI response: {json_error}")
                    response_data = {"error": {"message": f"Failed to parse response: {str(json_error)}"}}
                    success = False
            except Exception as e:
                success = False
                response = None
                logger.error(f"Error making OpenAI HTTP request: {str(e)}")
                raise
            finally:
                duration = time.time() - start_time
                
                # Only log if this wasn't already logged by the SDK
                if not getattr(request_data, '_tropir_logged', False):
                    logger.info(f"Logging direct OpenAI API call to: {url}")
                    
                    # Add URL to request data for proper logging
                    if isinstance(request_data, dict):
                        request_data["url"] = url
                    
                    # Log the detailed response
                    log_openai_call("openai", request_data, response, duration, success)
                    
                    # Mark as logged to prevent double-logging
                    if isinstance(request_data, dict):
                        request_data['_tropir_logged'] = True
            
            return response
        except Exception as e:
            logger.error(f"Error in patched httpx.AsyncClient.post for OpenAI: {str(e)}")
            logger.error(traceback.format_exc())
            # Always let the original request proceed even if tracking fails
            return await original_post(self, url, *args, **kwargs)
    else:
        # For non-OpenAI URLs, just call the original function
        return await original_post(self, url, *args, **kwargs)

def setup_http_patching():
    """Set up tracking specifically for direct HTTP calls to OpenAI API."""
    try:
        # Patch requests library for synchronous HTTP calls
        try:
            import requests
            if not getattr(requests.post, '_llm_tracker_patched_openai_http', False):
                logger.info("Patching requests.post for direct OpenAI API calls")
                original_post = requests.post
                
                # Create a wrapper that maintains the function signature
                @functools.wraps(original_post)
                def wrapper(*args, **kwargs):
                    return patched_requests_post(original_post, *args, **kwargs)
                
                # Mark as patched with a specific tag for HTTP patching
                wrapper._llm_tracker_patched_openai_http = True
                requests.post = wrapper
                logger.info("Successfully patched requests.post for direct OpenAI API calls")
            else:
                logger.info("requests.post already patched for direct OpenAI API calls")
        except ImportError:
            logger.debug("Could not import 'requests'. Direct HTTP patching for requests will be skipped.")
            
        # Patch httpx.AsyncClient for async HTTP calls
        try:
            import httpx
            
            if not getattr(httpx.AsyncClient.post, '_llm_tracker_patched_openai_http', False):
                logger.info("Patching httpx.AsyncClient.post for direct OpenAI API calls")
                
                # Store the original method
                original_async_post = httpx.AsyncClient.post
                
                # Create an async wrapper that maintains the function signature
                @functools.wraps(original_async_post)
                async def async_wrapper(self, url, *args, **kwargs):
                    return await patched_httpx_async_post(original_async_post, self, url, *args, **kwargs)
                
                # Mark as patched with a specific tag for HTTP patching
                async_wrapper._llm_tracker_patched_openai_http = True
                
                # Apply the patch
                httpx.AsyncClient.post = async_wrapper
                
                logger.info("Successfully patched httpx.AsyncClient.post for direct OpenAI API calls")
            else:
                logger.info("httpx.AsyncClient.post already patched for direct OpenAI API calls")
        except ImportError:
            logger.debug("Could not import 'httpx'. Direct HTTP patching for httpx will be skipped.")
            
    except Exception as e:
        logger.error(f"Failed to set up HTTP patching for OpenAI: {e}")
        logger.error(traceback.format_exc())

def setup_openai_patching():
    """Set up tracking for OpenAI by patching target methods."""
    try:
        # Import the specific class where the 'create' method resides
        from openai.resources.chat.completions import Completions as OpenAICompletions
        
        # Import beta chat completions
        try:
            from openai.resources.beta.chat.completions import Completions as BetaChatCompletions
            
            # Patch the parse method specifically since it has unique parameters
            if hasattr(BetaChatCompletions, "parse") and not getattr(BetaChatCompletions.parse, '_llm_tracker_patched', False):
                original_parse = BetaChatCompletions.parse
                
                @functools.wraps(original_parse)
                def patched_parse(self, *args, **kwargs):
                    # Skip if OpenRouter
                    if is_openrouter_request(client=self):
                        return original_parse(self, *args, **kwargs)
                    
                    # Handle response_format before passing to log
                    response_format = kwargs.get('response_format')
                    if response_format is not None:
                        # If it's a Pydantic model class, get its schema
                        if hasattr(response_format, 'model_json_schema'):
                            kwargs['_response_format_schema'] = response_format.model_json_schema()
                        # If it's some other class, get its name at minimum
                        else:
                            kwargs['_response_format_schema'] = {
                                "type": response_format.__name__ if hasattr(response_format, '__name__') else str(response_format)
                            }
                    
                    start_time = time.time()
                    success = True
                    try:
                        response = original_parse(self, *args, **kwargs)
                    except Exception as e:
                        success = False
                        response = None
                        logger.error(f"Error in OpenAI beta chat parse call: {str(e)}")
                        raise e
                    finally:
                        duration = time.time() - start_time
                        # Use the schema we stored instead of the actual response_format class
                        if '_response_format_schema' in kwargs:
                            kwargs['response_format'] = kwargs.pop('_response_format_schema')
                        log_openai_call("openai", kwargs, response, duration, success)
                    return response
                
                BetaChatCompletions.parse = patched_parse
                BetaChatCompletions.parse._llm_tracker_patched = True
                logger.info("Successfully patched beta.chat.completions.parse")
            
            # Patch the create method if it exists
            if hasattr(BetaChatCompletions, "create") and not getattr(BetaChatCompletions.create, '_llm_tracker_patched', False):
                original_create = BetaChatCompletions.create
                
                @functools.wraps(original_create)
                def patched_create(self, *args, **kwargs):
                    # Skip if OpenRouter
                    if is_openrouter_request(client=self):
                        return original_create(self, *args, **kwargs)
                    
                    start_time = time.time()
                    success = True
                    try:
                        response = original_create(self, *args, **kwargs)
                    except Exception as e:
                        success = False
                        response = None
                        logger.error(f"Error in OpenAI beta chat create call: {str(e)}")
                        raise e
                    finally:
                        duration = time.time() - start_time
                        log_openai_call("openai", kwargs, response, duration, success)
                    return response
                
                BetaChatCompletions.create = patched_create
                BetaChatCompletions.create._llm_tracker_patched = True
                logger.info("Successfully patched beta.chat.completions.create")
                
        except ImportError:
            logger.warning("Could not import OpenAI beta chat completions. Beta chat completions tracking will be skipped.")
        except Exception as e:
            logger.error(f"Failed during OpenAI beta chat completions patching: {e}")
            logger.error(traceback.format_exc())

        # Check if the 'create' method exists and hasn't been patched yet
        if hasattr(OpenAICompletions, "create") and not getattr(OpenAICompletions.create, '_llm_tracker_patched', False):
            original_create_method = OpenAICompletions.create  # Get the original function

            # Create a wrapper that first checks if this is an OpenRouter request
            @functools.wraps(original_create_method)
            def patched_create_method(self, *args, **kwargs):
                # Strong check for OpenRouter - if any of these conditions are true, skip this request
                is_openrouter = False
                
                # First check if this is marked as an OpenRouter client
                if hasattr(self, "_client") and getattr(self._client, "_is_openrouter_client", False):
                    is_openrouter = True
                    logger.debug("OpenAI patch skipping OpenRouter client (marked as OpenRouter)")
                
                # Check base_url
                if not is_openrouter and hasattr(self, "_client") and hasattr(self._client, "base_url"):
                    if is_openrouter_url(self._client.base_url):
                        is_openrouter = True
                        logger.debug(f"OpenAI patch skipping OpenRouter client with base_url: {self._client.base_url}")
                
                # Check model format
                if not is_openrouter and "model" in kwargs and isinstance(kwargs["model"], str) and "/" in kwargs["model"]:
                    model_parts = kwargs["model"].split("/")
                    if len(model_parts) >= 2 and model_parts[0] in ["openai", "anthropic", "google", "meta", "cohere"]:
                        is_openrouter = True
                        logger.debug(f"OpenAI patch skipping OpenRouter model: {kwargs['model']}")
                
                # If this is an OpenRouter request, skip it entirely
                if is_openrouter:
                    return original_create_method(self, *args, **kwargs)
                
                # Standard OpenAI request patching
                start_time = time.time()
                success = True
                try:
                    response = original_create_method(self, *args, **kwargs)
                except Exception as e:
                    success = False
                    response = None
                    logger.error(f"Error in OpenAI call: {str(e)}")
                    raise e
                finally:
                    duration = time.time() - start_time
                    log_openai_call("openai", kwargs, response, duration, success)
                return response

            # Replace the original method with the patched one
            OpenAICompletions.create = patched_create_method
            OpenAICompletions.create._llm_tracker_patched = True

        # Patch the responses methods
        try:
            from openai.resources.responses import Responses as OpenAIResponses
            from openai.resources.responses import AsyncResponses as AsyncOpenAIResponses

            # Patch synchronous Responses methods
            methods_to_patch = ['create', 'stream', 'parse', 'retrieve', 'delete']
            
            for method_name in methods_to_patch:
                if hasattr(OpenAIResponses, method_name) and not getattr(getattr(OpenAIResponses, method_name), '_llm_tracker_patched', False):
                    original_method = getattr(OpenAIResponses, method_name)
                    
                    # Create patched version that skips OpenRouter requests
                    @functools.wraps(original_method)
                    def patched_method(self, *args, **kwargs):
                        # Strong check for OpenRouter - if any of these conditions are true, skip this request
                        is_openrouter = False
                        
                        # First check if this is marked as an OpenRouter client
                        if hasattr(self, "_client") and getattr(self._client, "_is_openrouter_client", False):
                            is_openrouter = True
                            logger.debug("OpenAI responses patch skipping OpenRouter client (marked as OpenRouter)")
                        
                        # Check base_url
                        if not is_openrouter and hasattr(self, "_client") and hasattr(self._client, "base_url"):
                            if is_openrouter_url(self._client.base_url):
                                is_openrouter = True
                                logger.debug(f"OpenAI responses patch skipping OpenRouter client with base_url: {self._client.base_url}")
                        
                        # Check model format
                        if not is_openrouter and "model" in kwargs and isinstance(kwargs["model"], str) and "/" in kwargs["model"]:
                            model_parts = kwargs["model"].split("/")
                            if len(model_parts) >= 2 and model_parts[0] in ["openai", "anthropic", "google", "meta", "cohere"]:
                                is_openrouter = True
                                logger.debug(f"OpenAI responses patch skipping OpenRouter model: {kwargs['model']}")
                        
                        # If this is an OpenRouter request, skip it entirely
                        if is_openrouter:
                            return original_method(self, *args, **kwargs)
                        
                        # Standard OpenAI tracking
                        start_time = time.time()
                        success = True
                        try:
                            response = original_method(self, *args, **kwargs)
                        except Exception as e:
                            success = False
                            response = None
                            logger.error(f"Error in OpenAI {method_name} call: {str(e)}")
                            raise e
                        finally:
                            duration = time.time() - start_time
                            log_openai_call("openai", kwargs, response, duration, success)
                        return response
                    
                    setattr(OpenAIResponses, method_name, patched_method)
                    getattr(OpenAIResponses, method_name)._llm_tracker_patched = True

        except ImportError:
            logger.warning("Could not import OpenAI responses classes. OpenAI responses tracking may not work.")
        except Exception as e:
            logger.error(f"Failed during OpenAI responses patching: {e}")
            logger.error(traceback.format_exc())
            
        # Now set up HTTP patching - do this separately to avoid interference
        setup_http_patching()

    except ImportError:
        logger.warning("Could not import 'openai.resources.chat.completions.Completions'. Only direct API calls will be tracked.")
        # Set up HTTP patching even if SDK patching fails
        setup_http_patching()
    except Exception as e:
        logger.error(f"Failed during OpenAI patching process: {e}")
        logger.error(traceback.format_exc())
        # Attempt HTTP patching even if SDK patching fails
        setup_http_patching()