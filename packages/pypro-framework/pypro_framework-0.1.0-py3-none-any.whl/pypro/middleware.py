"""
Middleware module for PyPro.

This module provides a middleware system that allows for processing
requests before they reach the route handler and responses before they
are returned to the client.
"""

import time
import logging
from typing import Dict, List, Callable, Any, Optional, Union

from .types import Request, Response


class Middleware:
    """Base class for all middleware."""
    
    def process_request(self, request: Request) -> Request:
        """
        Process a request before it reaches the route handler.
        
        Args:
            request: The request object
            
        Returns:
            Modified request object
        """
        return request
    
    def process_response(self, request: Request, response: Response) -> Response:
        """
        Process a response before it is returned to the client.
        
        Args:
            request: The request object
            response: The response object
            
        Returns:
            Modified response object
        """
        return response


class MiddlewareStack:
    """
    Stack of middleware to be applied in order.
    
    Middleware is processed in the order it is added for requests,
    and in reverse order for responses.
    """
    
    def __init__(self):
        self.middleware = []
    
    def add(self, middleware: Middleware):
        """
        Add middleware to the stack.
        
        Args:
            middleware: Middleware instance to add
        """
        self.middleware.append(middleware)
    
    def process_request(self, request: Request) -> Request:
        """
        Process a request through all middleware.
        
        Args:
            request: The request object
            
        Returns:
            Modified request object
        """
        for middleware in self.middleware:
            request = middleware.process_request(request)
        return request
    
    def process_response(self, request: Request, response: Response) -> Response:
        """
        Process a response through all middleware in reverse order.
        
        Args:
            request: The request object
            response: The response object
            
        Returns:
            Modified response object
        """
        for middleware in reversed(self.middleware):
            response = middleware.process_response(request, response)
        return response


# Useful built-in middleware

class LoggingMiddleware(Middleware):
    """Middleware for logging requests and responses."""
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger('pypro.middleware.logging')
    
    def process_request(self, request: Request) -> Request:
        """Log incoming request details."""
        request._start_time = time.time()
        self.logger.info(f"Request: {request.method} {request.path}")
        return request
    
    def process_response(self, request: Request, response: Response) -> Response:
        """Log response details."""
        duration = time.time() - getattr(request, '_start_time', time.time())
        self.logger.info(
            f"Response: {response.status_code} "
            f"({duration:.3f}s)"
        )
        return response


class SessionMiddleware(Middleware):
    """Middleware for handling sessions."""
    
    def __init__(self, app, cookie_name='session', secure=False):
        self.app = app
        self.cookie_name = cookie_name
        self.secure = secure
    
    def process_request(self, request: Request) -> Request:
        """Load session data from cookie."""
        session_id = request.cookies.get(self.cookie_name)
        
        if session_id and session_id in self.app.session_store:
            request.session = self.app.session_store[session_id]
        else:
            # Create a new session
            from .utils import generate_id
            session_id = generate_id()
            self.app.session_store[session_id] = {}
            request.session = self.app.session_store[session_id]
            
        request._session_id = session_id
        return request
    
    def process_response(self, request: Request, response: Response) -> Response:
        """Save session data to cookie if modified."""
        session_id = getattr(request, '_session_id', None)
        
        if session_id:
            # Update session store
            self.app.session_store[session_id] = request.session
            
            # Set session cookie
            response.set_cookie(
                self.cookie_name,
                session_id,
                secure=self.secure,
                http_only=True,
                max_age=86400  # 24 hours
            )
            
        return response


class CSRFMiddleware(Middleware):
    """Middleware for CSRF protection."""
    
    def __init__(self, app, csrf_token_name='_csrf_token', form_field='_csrf_token'):
        self.app = app
        self.csrf_token_name = csrf_token_name
        self.form_field = form_field
    
    def process_request(self, request: Request) -> Request:
        """
        Generate or validate CSRF token.
        
        For GET requests, a token is generated if one doesn't exist.
        For POST/PUT/DELETE requests, the token is validated.
        """
        # Skip CSRF checks for AJAX requests with X-Requested-With header
        is_ajax = request.environ.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        
        # Initialize session if needed
        if not hasattr(request, 'session'):
            request.session = {}
            
        # Generate token for GET requests
        if request.method == 'GET':
            if self.csrf_token_name not in request.session:
                from .security import generate_csrf_token
                request.session[self.csrf_token_name] = generate_csrf_token()
        
        # Validate token for state-changing requests
        elif request.method in ('POST', 'PUT', 'DELETE') and not is_ajax:
            # Get token from form data
            form_token = request.form_data.get(self.form_field, [''])[0]
            
            # Get token from session
            session_token = request.session.get(self.csrf_token_name)
            
            # Check if tokens match
            from .security import validate_csrf
            if not validate_csrf(form_token, session_token):
                error_page = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>403 Forbidden</title>
                </head>
                <body>
                    <h1>403 Forbidden</h1>
                    <p>CSRF token validation failed.</p>
                </body>
                </html>
                """
                raise Exception("CSRF token validation failed.")
                
        return request


class CORSMiddleware(Middleware):
    """Middleware for Cross-Origin Resource Sharing (CORS)."""
    
    def __init__(self, allow_origins=None, allow_methods=None, 
                 allow_headers=None, allow_credentials=False, max_age=86400):
        self.allow_origins = allow_origins or []
        self.allow_methods = allow_methods or ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
        self.allow_headers = allow_headers or ['Content-Type', 'Authorization']
        self.allow_credentials = allow_credentials
        self.max_age = max_age
    
    def process_response(self, request: Request, response: Response) -> Response:
        """Add CORS headers to response."""
        origin = request.environ.get('HTTP_ORIGIN')
        
        # Skip if no origin header or origin not allowed
        if not origin or (self.allow_origins and origin not in self.allow_origins and '*' not in self.allow_origins):
            return response
            
        # Add CORS headers
        headers = response.headers
        headers['Access-Control-Allow-Origin'] = origin if origin in self.allow_origins else '*'
        
        if self.allow_credentials:
            headers['Access-Control-Allow-Credentials'] = 'true'
            
        # Handle preflight requests
        if request.method == 'OPTIONS':
            headers['Access-Control-Allow-Methods'] = ', '.join(self.allow_methods)
            headers['Access-Control-Allow-Headers'] = ', '.join(self.allow_headers)
            headers['Access-Control-Max-Age'] = str(self.max_age)
            
        return response


class RateLimitingMiddleware(Middleware):
    """Middleware for rate limiting requests."""
    
    def __init__(self, max_requests=100, time_window=60):
        self.max_requests = max_requests
        self.time_window = time_window  # seconds
        self.request_logs = {}  # ip -> [timestamps]
        
    def process_request(self, request: Request) -> Request:
        """
        Check if the request exceeds the rate limit.
        
        Args:
            request: The request object
            
        Returns:
            The request object if allowed, raises an exception if rate limited
            
        Raises:
            Exception: If the request exceeds the rate limit
        """
        # Get client IP
        ip = request.environ.get('REMOTE_ADDR', 'unknown')
        
        # Get current time
        now = time.time()
        
        # Initialize request log for this IP if not exists
        if ip not in self.request_logs:
            self.request_logs[ip] = []
            
        # Remove timestamps older than the time window
        self.request_logs[ip] = [ts for ts in self.request_logs[ip] if now - ts <= self.time_window]
        
        # Check if max requests exceeded
        if len(self.request_logs[ip]) >= self.max_requests:
            error_page = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>429 Too Many Requests</title>
            </head>
            <body>
                <h1>429 Too Many Requests</h1>
                <p>Rate limit exceeded. Please try again later.</p>
            </body>
            </html>
            """
            raise Exception("Rate limit exceeded.")
            
        # Log this request
        self.request_logs[ip].append(now)
        
        return request
