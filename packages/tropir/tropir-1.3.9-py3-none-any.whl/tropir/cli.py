"""
Command-line interface for the Tropir Agent.
"""
import os
import sys
import uuid
import logging
import importlib.util
import runpy
import argparse
import re
from pathlib import Path
from contextlib import contextmanager
from loguru import logger

# Initialize with the request_id context variable
from sublingual_eval.logging.openai_logger import request_id_ctx_var

def setup_flask_logging():
    """Set up request ID tracking for Flask applications."""
    try:
        from flask import Flask
    except ImportError:
        return False

    if getattr(Flask.__init__, '_is_request_id_patched', False):
        return True

    original_init = Flask.__init__
    def custom_init(self, *args, **kwargs):
        # Initialize the Flask app normally
        original_init(self, *args, **kwargs)
        # Only patch the wsgi_app if not already patched
        if not getattr(self.wsgi_app, '_is_request_id_patched', False):
            original_wsgi_app = self.wsgi_app
            def custom_wsgi_app(environ, start_response):
                token = request_id_ctx_var.set(str(uuid.uuid4()))
                try:
                    return original_wsgi_app(environ, start_response)
                finally:
                    request_id_ctx_var.reset(token)
            # Mark the wsgi_app wrapper as patched to prevent duplication
            custom_wsgi_app._is_request_id_patched = True
            self.wsgi_app = custom_wsgi_app

    # Mark our custom __init__ so we don't patch twice
    custom_init._is_request_id_patched = True
    Flask.__init__ = custom_init
    return True

def setup_django_asgi_logging():
    """Set up request ID tracking for Django ASGI applications."""
    try:
        from django.core.handlers.asgi import ASGIHandler
        # Check if already patched
        if getattr(ASGIHandler.__call__, '_is_request_id_patched', False):
            return True

        original_asgi_call = ASGIHandler.__call__
        async def custom_asgi_call(self, scope, receive, send):
            token = request_id_ctx_var.set(str(uuid.uuid4()))
            try:
                response = await original_asgi_call(self, scope, receive, send)
                return response
            finally:
                request_id_ctx_var.reset(token)

        # Mark the patched function to avoid double patching
        custom_asgi_call._is_request_id_patched = True
        ASGIHandler.__call__ = custom_asgi_call
        return True
    except ImportError:
        return False

def setup_django_wsgi_logging():
    """Set up request ID tracking for Django WSGI applications."""
    try:
        from django.core.handlers.wsgi import WSGIHandler
        # Check if already patched
        if getattr(WSGIHandler.__call__, '_is_request_id_patched', False):
            return True

        original_wsgi_call = WSGIHandler.__call__
        def custom_wsgi_call(self, environ, start_response):
            token = request_id_ctx_var.set(str(uuid.uuid4()))
            try:
                response = original_wsgi_call(self, environ, start_response)
                return response
            finally:
                request_id_ctx_var.reset(token)

        # Mark the patched function to avoid double patching
        custom_wsgi_call._is_request_id_patched = True
        WSGIHandler.__call__ = custom_wsgi_call
        return True
    except ImportError:
        return False

def setup_fastapi_logging():
    """Set up request ID tracking for FastAPI applications."""
    try:
        from fastapi import FastAPI
        from fastapi.routing import APIRoute
        from starlette.middleware.base import BaseHTTPMiddleware
        
        # Check if already patched
        if getattr(APIRoute.get_route_handler, '_is_request_id_patched', False):
            return True

        # Create middleware class for request ID tracking
        class RequestIDMiddleware(BaseHTTPMiddleware):
            async def dispatch(self, request, call_next):
                # Generate and set request ID
                request_id = str(uuid.uuid4())
                token = request_id_ctx_var.set(request_id)
                
                # Add request ID header for debugging
                try:
                    response = await call_next(request)
                    response.headers["X-Request-ID"] = request_id
                    return response
                finally:
                    request_id_ctx_var.reset(token)
        
        # Patch the FastAPI app initialization to add middleware
        original_init = FastAPI.__init__
        def custom_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            # Add middleware at the beginning of the chain
            self.add_middleware(RequestIDMiddleware)
        
        # Mark the patched function
        custom_init._is_request_id_patched = True
        FastAPI.__init__ = custom_init
        
        # Also patch the route handler for backward compatibility
        original_get_route_handler = APIRoute.get_route_handler
        def custom_get_route_handler(self):
            original_handler = original_get_route_handler(self)
            async def custom_handler(request):
                # If no request ID is set from middleware, set one here
                if request_id_ctx_var.get(None) is None:
                    token = request_id_ctx_var.set(str(uuid.uuid4()))
                    try:
                        response = await original_handler(request)
                        return response
                    finally:
                        request_id_ctx_var.reset(token)
                else:
                    # Use existing request ID set by middleware
                    return await original_handler(request)
            return custom_handler
        
        # Mark the patched function
        custom_get_route_handler._is_request_id_patched = True
        APIRoute.get_route_handler = custom_get_route_handler
        
        return True
    except ImportError:
        return False

def setup_logging():
    """Set up request ID tracking for all supported web frameworks."""
    flask_setup = setup_flask_logging()
    django_asgi_setup = setup_django_asgi_logging()
    django_wsgi_setup = setup_django_wsgi_logging()
    fastapi_setup = setup_fastapi_logging()
    
    logger.debug(f"Framework integrations: Flask={flask_setup}, Django ASGI={django_asgi_setup}, "
                f"Django WSGI={django_wsgi_setup}, FastAPI={fastapi_setup}")

def load_env_vars():
    """Load Tropir environment variables from .env file."""
    try:
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
    except Exception as e:
        pass

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Tropir Agent CLI")
    parser.add_argument('command', help='Command to run with Tropir agent enabled')
    parser.add_argument('args', nargs=argparse.REMAINDER, help='Arguments for the command')
    
    args = parser.parse_args()
    
    # Enable Tropir tracking
    os.environ["TROPIR_ENABLED"] = "1"
    
    # Load environment variables
    load_env_vars()
    
    # Initialize the agent and setup logging
    from . import initialize
    initialize()
    setup_logging()
    
    # Add the current directory to the Python path
    sys.path.insert(0, os.getcwd())
    
    # Run the command
    if args.command == "python":
        if len(args.args) > 0:
            if args.args[0] == "-m":
                # Handle module execution
                if len(args.args) > 1:
                    module_name = args.args[1]
                    sys.argv = [args.args[0]] + args.args[1:]
                    try:
                        runpy.run_module(module_name, run_name="__main__")
                    except ModuleNotFoundError as e:
                        print(f"Error: {e}")
                        print("Make sure you're running this command from the correct directory.")
                        sys.exit(1)
                else:
                    print("Missing module name")
                    sys.exit(1)
            else:
                # Handle script execution
                script_path = args.args[0]
                sys.argv = args.args
                try:
                    runpy.run_path(script_path, run_name="__main__")
                except FileNotFoundError:
                    print(f"Error: File '{script_path}' not found.")
                    sys.exit(1)
        else:
            print("Missing python script or module")
            sys.exit(1)
    elif args.command == "uvicorn":
        # Handle uvicorn command
        if len(args.args) > 0:
            sys.argv = [args.command] + args.args
            try:
                runpy.run_module("uvicorn", run_name="__main__")
            except ModuleNotFoundError:
                print("Error: Uvicorn is not installed. Please install it with 'pip install uvicorn'.")
                sys.exit(1)
        else:
            print("Missing uvicorn arguments. Usage: tropir uvicorn app:app [--host 0.0.0.0] [--port 8000] [...]")
            sys.exit(1)
    elif args.command == "flask":
        # Handle flask command
        if len(args.args) > 0:
            sys.argv = [args.command] + args.args
            try:
                runpy.run_module("flask.cli", run_name="__main__")
            except ModuleNotFoundError:
                print("Error: Flask is not installed. Please install it with 'pip install flask'.")
                sys.exit(1)
        else:
            print("Missing flask arguments. Usage: tropir flask run [--host=0.0.0.0] [--port=5000] [...]")
            sys.exit(1)
    else:
        print(f"Unsupported command: {args.command}")
        sys.exit(1)

if __name__ == "__main__":
    main()