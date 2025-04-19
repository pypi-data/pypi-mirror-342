"""
Tropir.
"""

from .bedrock_patch import setup_bedrock_patching
from .openai_patch import setup_openai_patching
from .anthropic_patch import setup_anthropic_patching
from .openrouter_patch import setup_openrouter_patching
import os
import sys
import requests
from loguru import logger

from .config import DEFAULT_API_URL

def initialize():
    # Load only TROPIR environment variables from .env file if available
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
                            if key == "TROPIR_API_KEY":
                                print("Successfully loaded TROPIR_API_KEY from environment variables.")
                            elif key == "TROPIR_API_URL":
                                print("Successfully loaded TROPIR_API_URL from environment variables.")
    except Exception as e:
        print(f"Warning: Could not load TROPIR environment variables: {e}")
    
    # Validate API key before proceeding
    api_key = os.environ.get("TROPIR_API_KEY")
    if not api_key:
        print("Error: TROPIR_API_KEY environment variable not set. Tropir cannot run without a valid API key.")
        sys.exit(1)
    
    # Validate the API key by making a request to the server
    try:
        base_url = os.environ.get("TROPIR_API_URL", DEFAULT_API_URL)
        endpoint = f"{base_url}api/api-key"
        
        response = requests.post(
            endpoint,
            json={"api_key": api_key},
            timeout=10.0
        )
        
        response.raise_for_status()
        
        if not response.text:
            print("Error: Empty response received during API key validation.")
            sys.exit(1)
            
        result = response.json()
        
        if result.get("status") == "ok" and "user_id" in result:
            user_id = result.get("user_id")
            os.environ["TROPIR_USER_ID"] = user_id
            print("API key validated successfully.")
        else:
            error_msg = result.get("message", "Unknown error")
            print(f"Error: API key validation failed: {error_msg}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as req_err:
        print(f"Error: Failed to connect to Tropir API: {req_err}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to validate API key: {str(e)}")
        sys.exit(1)
    
    setup_openai_patching() 
    setup_bedrock_patching()
    setup_anthropic_patching()
    setup_openrouter_patching()