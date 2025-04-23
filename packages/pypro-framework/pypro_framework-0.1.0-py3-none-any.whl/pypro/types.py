"""
Type definitions for PyPro.

This module contains shared type definitions to avoid circular imports.
"""
import json
from typing import Dict, Any, List, Optional, Union
from urllib.parse import parse_qs

class Request:
    """Request object to encapsulate WSGI environment."""
    
    def __init__(self, environ: Dict[str, Any]):
        self.environ = environ
        self.path = environ.get('PATH_INFO', '/')
        self.method = environ.get('REQUEST_METHOD', 'GET')
        self.query_params = parse_qs(environ.get('QUERY_STRING', ''))
        self.form_data = {}
        self.cookies = {}
        self.session = {}
        
        # Parse cookies
        cookie_string = environ.get('HTTP_COOKIE', '')
        if cookie_string:
            for cookie in cookie_string.split(';'):
                if '=' in cookie:
                    name, value = cookie.strip().split('=', 1)
                    self.cookies[name] = value
        
        # Parse form data if content type is form
        if self.method in ('POST', 'PUT') and environ.get('CONTENT_TYPE', '').startswith('application/x-www-form-urlencoded'):
            content_length = int(environ.get('CONTENT_LENGTH', '0'))
            if content_length:
                form_data = environ['wsgi.input'].read(content_length).decode('utf-8')
                self.form_data = parse_qs(form_data)
        
        # Parse JSON if content type is JSON
        if self.method in ('POST', 'PUT') and environ.get('CONTENT_TYPE', '').startswith('application/json'):
            content_length = int(environ.get('CONTENT_LENGTH', '0'))
            if content_length:
                json_data = environ['wsgi.input'].read(content_length).decode('utf-8')
                try:
                    self.json = json.loads(json_data)
                except json.JSONDecodeError:
                    self.json = {}

    def get_data(self, key, default=None):
        """Get data from query parameters or form data."""
        if key in self.query_params:
            return self.query_params[key][0]
        if key in self.form_data:
            return self.form_data[key][0]
        return default
    
    def get_json(self):
        """Get JSON data if available."""
        return getattr(self, 'json', None)


class Response:
    """Response object to encapsulate HTTP response."""
    
    def __init__(self, body='', status_code=200, headers=None, content_type='text/html'):
        self.body = body
        self.status_code = status_code
        self.headers = headers or {}
        
        # Make sure Content-Type is set
        if 'Content-Type' not in self.headers:
            self.headers['Content-Type'] = content_type
    
    def set_cookie(self, name, value, max_age=None, expires=None, path='/', 
                  domain=None, secure=False, http_only=True):
        """Set a cookie in the response."""
        cookie = f"{name}={value}"
        
        if max_age is not None:
            cookie += f"; Max-Age={max_age}"
        if expires is not None:
            cookie += f"; Expires={expires}"
        if path:
            cookie += f"; Path={path}"
        if domain:
            cookie += f"; Domain={domain}"
        if secure:
            cookie += "; Secure"
        if http_only:
            cookie += "; HttpOnly"
            
        self.headers['Set-Cookie'] = cookie
    
    def to_wsgi(self):
        """Convert response to WSGI format."""
        if isinstance(self.body, str):
            body = self.body.encode('utf-8')
        elif isinstance(self.body, bytes):
            body = self.body
        else:
            body = str(self.body).encode('utf-8')
            
        status = f"{self.status_code} {self._status_message(self.status_code)}"
        headers = list(self.headers.items())
        
        return status, headers, [body]
    
    @staticmethod
    def _status_message(code):
        """Get HTTP status message for a code."""
        messages = {
            200: 'OK',
            201: 'Created',
            204: 'No Content',
            301: 'Moved Permanently',
            302: 'Found',
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not Found',
            405: 'Method Not Allowed',
            500: 'Internal Server Error',
        }
        return messages.get(code, 'Unknown')
    
    @classmethod
    def json(cls, data, status_code=200, headers=None):
        """Create a JSON response."""
        body = json.dumps(data)
        headers = headers or {}
        headers['Content-Type'] = 'application/json'
        return cls(body, status_code, headers)
    
    @classmethod
    def redirect(cls, location, status_code=302, headers=None):
        """Create a redirect response."""
        headers = headers or {}
        headers['Location'] = location
        return cls('', status_code, headers)