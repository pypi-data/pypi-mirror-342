"""
Tropir.
"""

from .bedrock_patch import setup_bedrock_patching
from .openai_patch import setup_openai_patching
from .anthropic_patch import setup_anthropic_patching
from .openrouter_patch import setup_openrouter_patching
import os
import sys

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
    
    setup_openai_patching() 
    setup_bedrock_patching()
    setup_anthropic_patching()
    setup_openrouter_patching()