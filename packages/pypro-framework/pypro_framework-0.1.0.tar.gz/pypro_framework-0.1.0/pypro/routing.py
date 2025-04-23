"""
Routing module for PyPro.

This module provides a URL routing system similar to Flask, with support for
URL parameters, path variables, and HTTP method filtering.
"""

import re
from typing import Dict, Any, Callable, List, Tuple, Optional

# Global routes dictionary to support url_for function
_global_routes = {}

class Router:
    """URL router for the PyPro application."""
    
    def __init__(self):
        self.routes = []
        
    def add_route(self, path: str, handler: Callable, methods: List[str] = None):
        """
        Add a route to the router.
        
        Args:
            path: URL path pattern with optional parameters like /<param> or /<param:type>
            handler: Function to execute when route matches
            methods: List of HTTP methods this route accepts
        """
        methods = methods or ['GET']
        
        # Convert Flask-style routing patterns to regex
        pattern = self._path_to_regex(path)
        
        # Store route info
        route_info = {
            'path': path,
            'pattern': pattern,
            'handler': handler,
            'methods': [m.upper() for m in methods],
            'endpoint': handler.__name__,
        }
        
        self.routes.append(route_info)
        
        # Register in global routes for url_for
        _global_routes[handler.__name__] = route_info
    
    def url_for(self, endpoint: str, **params) -> str:
        """
        Generate a URL for a given endpoint and parameters.
        
        Args:
            endpoint: Function name of the route handler
            **params: Parameters to substitute in the URL
            
        Returns:
            URL string with parameters substituted
        """
        for route in self.routes:
            if route['endpoint'] == endpoint:
                path = route['path']
                # Replace parameters in path
                for name, value in params.items():
                    path = path.replace(f'<{name}>', str(value))
                    path = path.replace(f'<int:{name}>', str(value))
                    path = path.replace(f'<path:{name}>', str(value))
                    path = path.replace(f'<string:{name}>', str(value))
                return path
        
        # No route found for endpoint
        return '/'
        
    def match_route(self, path: str, method: str) -> Tuple[Optional[Callable], Dict[str, Any]]:
        """
        Match a path and method to a route handler.
        
        Args:
            path: The URL path to match
            method: The HTTP method
            
        Returns:
            Tuple of (handler_function, params_dict) if route matches,
            otherwise (None, {})
        """
        method = method.upper()
        
        for route in self.routes:
            # Check if method is allowed
            if method not in route['methods']:
                continue
                
            # Try to match the pattern
            match = route['pattern'].match(path)
            if match:
                params = match.groupdict()
                # Convert param types based on annotations (if any)
                handler = route['handler']
                if hasattr(handler, '__annotations__'):
                    for param, param_type in handler.__annotations__.items():
                        if param in params and param != 'return':
                            try:
                                params[param] = param_type(params[param])
                            except (ValueError, TypeError):
                                # If type conversion fails, keep as string
                                pass
                return handler, params
        
        return None, {}
    
    def _path_to_regex(self, path: str) -> re.Pattern:
        """
        Convert a Flask-style path pattern to a regex pattern.
        
        Handles patterns like:
        - /users/<id>
        - /users/<int:id>
        - /users/<path:filepath>
        """
        # Handle static paths
        if '<' not in path:
            if path.endswith('/'):
                # Make trailing slash optional
                path = path[:-1]
                return re.compile(f'^{re.escape(path)}/?$')
            return re.compile(f'^{re.escape(path)}$')
        
        # Prepare regex parts
        regex_parts = []
        parts = path.split('/')
        
        for part in parts:
            if not part:
                continue
                
            if '<' in part and '>' in part:
                # Extract the parameter specification
                param_match = re.match(r'<(?:([a-z]+):)?([a-zA-Z0-9_]+)>', part)
                if param_match:
                    param_type, param_name = param_match.groups()
                    
                    # Map param types to regex patterns
                    if param_type == 'int':
                        pattern = r'(?P<{}>\\d+)'.format(param_name)
                    elif param_type == 'float':
                        pattern = r'(?P<{}>[+-]?\\d+\\.\\d+)'.format(param_name)
                    elif param_type == 'path':
                        pattern = r'(?P<{}>.+)'.format(param_name)
                    else:  # Default: string
                        pattern = r'(?P<{}>[^/]+)'.format(param_name)
                        
                    regex_parts.append(pattern)
                else:
                    # Invalid parameter format, treat as literal
                    regex_parts.append(re.escape(part))
            else:
                # Regular path segment
                regex_parts.append(re.escape(part))
        
        # Join parts with slashes
        regex = '^/' + '/'.join(regex_parts) + '/?$'
        return re.compile(regex)


def route(path, methods=None):
    """
    Route decorator for global usage outside PyProApp.
    
    This function stores decorated functions in a global registry
    that can be later added to a PyProApp instance.
    
    Example:
        @route('/users/<id>')
        def get_user(req, id):
            return f"User {id}"
    """
    methods = methods or ['GET']
    
    def decorator(handler):
        # Store original attributes for later
        handler._pypro_route = {
            'path': path,
            'methods': methods,
        }
        return handler
        
    return decorator


def url_for(endpoint: str, **params) -> str:
    """
    Generate a URL for a given endpoint and parameters.
    
    Args:
        endpoint: Function name of the route handler
        **params: Parameters to substitute in the URL
        
    Returns:
        URL string with parameters substituted
    """
    if endpoint not in _global_routes:
        raise ValueError(f"No route found for endpoint '{endpoint}'")
    
    route_info = _global_routes[endpoint]
    path = route_info['path']
    
    # Replace parameters in the path
    for param_name, param_value in params.items():
        path = path.replace(f'<{param_name}>', str(param_value))
        path = path.replace(f'<int:{param_name}>', str(param_value))
        path = path.replace(f'<float:{param_name}>', str(param_value))
        path = path.replace(f'<path:{param_name}>', str(param_value))
    
    return path
