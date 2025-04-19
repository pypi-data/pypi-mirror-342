"""
Transport module for sending logs to Tropir API.
"""

import os
import requests
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
            
        # Include the API key in the request
        requests.post(
            config["api_url"],
            json={"api_key": api_key, "log_data": log_data},
            timeout=3
        )
    except Exception as e:
        print(f"[TROPIR ERROR] Failed to send log: {e}") 