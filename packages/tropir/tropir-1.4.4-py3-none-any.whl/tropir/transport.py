"""
Transport module for sending logs to Tropir API.
"""

import os
import json
import requests
import traceback
import sys
from datetime import datetime
from .config import get_config


def send_log(log_data):
    """
    Sends log data to the Tropir API.
    
    Args:
        log_data (dict): The log data to send
    """
    config = get_config()
    if not config["enabled"]:
        return
    try:
        # Get API key from environment variables
        api_key = os.environ.get("TROPIR_API_KEY")
        if not api_key:
            print("[TROPIR ERROR] API key not found in environment variables")
            return
        
        # Add timestamp for tracking
        log_data["timestamp"] = datetime.now().isoformat()
        
        # Enhance with URL information for HTTP requests
        request_data = log_data.get('request', {})
        if isinstance(request_data, dict):
            url = request_data.get('url')
            if url and isinstance(url, str):
                # Try to extract domain for provider detection
                if "api.openai.com" in url:
                    log_data["provider"] = "openai"
                elif "api.anthropic.com" in url:
                    log_data["provider"] = "anthropic"
                elif "openrouter.ai" in url:
                    log_data["provider"] = "openrouter"
        
        # Ensure we have all required fields
        if "provider" not in log_data:
            log_data["provider"] = "unknown"
            
        if "response" not in log_data:
            log_data["response"] = ""
            
        # Prepare the payload
        payload = {
            "api_key": api_key,
            "log_data": log_data
        }
        
        # Send the request
        response = requests.post(
            config["api_url"],
            json=payload,
            timeout=5
        )
        
        # Check response status
        if response.status_code >= 300:
            print(f"[TROPIR ERROR] API returned error status: {response.status_code}")
    except requests.RequestException as e:
        print(f"[TROPIR ERROR] Network error sending log: {e}")
    except json.JSONDecodeError as e:
        print(f"[TROPIR ERROR] JSON encoding error: {e}")
    except Exception as e:
        print(f"[TROPIR ERROR] Failed to send log: {e}") 