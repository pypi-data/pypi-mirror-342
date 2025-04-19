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
        requests.post(
            config["api_url"],
            json=log_data,
            timeout=3
        )
    except Exception as e:
        print(f"[TROPIR ERROR] Failed to send log: {e}") 