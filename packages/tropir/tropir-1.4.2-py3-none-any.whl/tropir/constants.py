import contextvars
import threading
import uuid
from pathlib import Path

# Generate a unique session ID for this process
DEFAULT_SESSION_ID = str(uuid.uuid4())

# Patterns to exclude from stack trace analysis
EXCLUDED_STACK_FRAME_PATTERNS = [
    '<frozen',
    'site-packages',
    'dist-packages',
    'lib/python',
]

# Dictionary keys for token counting
TOKEN_COUNT_KEYS = {
    "PROMPT_TOKENS": "prompt_tokens",
    "COMPLETION_TOKENS": "completion_tokens",
    "TOTAL_TOKENS": "total_tokens"
}

# Model prefixes
ANTHROPIC_MODEL_PREFIXES = ["claude-", "anthropic."]

# Default token counts when counting fails
DEFAULT_TOKEN_COUNT = {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0
} 

SOURCE_CACHE = {}

# Context variable for request tracking
request_id_ctx_var = contextvars.ContextVar("request_id", default=None)

# Thread-local storage for tracking session IDs
_thread_local = threading.local()

# Use the constant for default session ID
_process_default_session_id = DEFAULT_SESSION_ID
