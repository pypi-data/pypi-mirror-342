"""
PyPro - A Flask-like web framework with batteries included.
"""

__version__ = '0.1.0'

# Import core components to make them available at the top level
from .types import Request, Response
from .app import PyProApp
from .routing import route, url_for
from .templating import render_template
# Database components will be imported here when implemented
# from .db import Model, Column, String, Integer, Boolean, DateTime, ForeignKey, relationship
from .security import generate_password_hash, check_password_hash, create_token, verify_token
from .middleware import Middleware, SessionMiddleware, CSRFMiddleware, LoggingMiddleware, CORSMiddleware, RateLimitingMiddleware
from .plugins import register_plugin, get_plugins
from .cli_simplified import main as cli_main

# Expose CLI main entry point
def main():
    """Main entry point for the PyPro CLI."""
    import sys
    sys.exit(cli_main())
