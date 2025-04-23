"""
Core application module for PyPro.
"""

import os
import sys
import json
import logging
import signal
import socket
from wsgiref.simple_server import make_server, WSGIRequestHandler
from typing import Dict, Any, List, Callable, Optional, Type, Union

from .types import Request, Response
from .routing import Router
from .templating import TemplateEngine
from .middleware import MiddlewareStack
from .plugins import get_plugins, PluginManager, hook


class ErrorHandler:
    """Handle errors and exceptions in the application."""
    
    def __init__(self, app):
        self.app = app
        
        # Default error handlers
        self.error_handlers = {
            404: self._default_404_handler,
            500: self._default_500_handler,
        }
    
    def register(self, code_or_exception, handler):
        """Register an error handler."""
        self.error_handlers[code_or_exception] = handler
    
    def handle_error(self, error, request):
        """Handle an error or exception."""
        if isinstance(error, Exception):
            # Log the exception for debugging
            logging.exception(error)
            
            # Check for specific exception handler
            for exc_type, handler in self.error_handlers.items():
                if isinstance(exc_type, type) and isinstance(error, exc_type):
                    return handler(request, error)
            
            # Fall back to general 500 handler
            return self.error_handlers.get(500, self._default_500_handler)(request, error)
        else:
            # Handle HTTP error code
            return self.error_handlers.get(error, self._default_404_handler)(
                request, error)
    
    def _default_404_handler(self, request, error=None):
        """Default handler for 404 errors."""
        return Response(
            "<h1>404 Not Found</h1>"
            f"<p>The requested URL {request.path} was not found on this server.</p>",
            404
        )
    
    def _default_500_handler(self, request, error=None):
        """Default handler for 500 errors."""
        error_details = str(error) if self.app.config['DEBUG'] else ''
        return Response(
            "<h1>500 Internal Server Error</h1>"
            f"<p>The server encountered an internal error.</p>"
            f"<p>{error_details}</p>",
            500
        ) if self.app.config['DEBUG'] else Response("<h1>500 Internal Server Error</h1>", 500)


class PyProApp:
    """Main application class for PyPro."""
    
    def __init__(self, import_name, template_folder='templates', static_folder='static', public_folder='public'):
        self.import_name = import_name
        self.template_folder = template_folder
        self.static_folder = static_folder
        self.public_folder = public_folder
        
        # Initialize core components
        self.router = Router()
        self.template_engine = TemplateEngine(self)
        self.middleware_stack = MiddlewareStack()
        self.error_handler = ErrorHandler(self)
        
        # Configuration
        self.config = {
            'DEBUG': False,
            'SECRET_KEY': os.environ.get('SECRET_KEY', 'dev_key'),
            'DATABASE_URL': os.environ.get('DATABASE_URL', 'sqlite:///pypro.db'),
            'PLUGINS_ENABLED': True,  # Enable plugins by default
        }
        
        # Session store
        self.session_store = {}
        
        # Plugin manager
        self.plugin_manager = PluginManager(self)
        
        # Set up static file serving
        self.router.add_route(
            f"/{self.static_folder}/<path:filename>", 
            self._serve_static, 
            methods=['GET']
        )
        
        # Set up public file serving
        self.router.add_route(
            f"/<path:filename>", 
            self._serve_public, 
            methods=['GET']
        )
        
    def _get_content_type(self, filename):
        """Determine content type based on file extension."""
        content_type = 'application/octet-stream'
        if filename.endswith('.css'):
            content_type = 'text/css'
        elif filename.endswith('.js'):
            content_type = 'application/javascript'
        elif filename.endswith('.html'):
            content_type = 'text/html'
        elif filename.endswith('.svg'):
            content_type = 'image/svg+xml'
        elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
            content_type = 'image/jpeg'
        elif filename.endswith('.png'):
            content_type = 'image/png'
        elif filename.endswith('.gif'):
            content_type = 'image/gif'
        elif filename.endswith('.json'):
            content_type = 'application/json'
        elif filename.endswith('.pdf'):
            content_type = 'application/pdf'
        elif filename.endswith('.txt'):
            content_type = 'text/plain'
        elif filename.endswith('.xml'):
            content_type = 'application/xml'
        return content_type
    
    def _serve_static(self, request, filename):
        """Serve static files from the static folder."""
        base_dir = os.path.dirname(sys.modules[self.import_name].__file__)
        filepath = os.path.join(base_dir, self.static_folder, filename)
        
        if not os.path.exists(filepath) or not os.path.isfile(filepath):
            return Response("<h1>404 Not Found</h1>", 404)
        
        with open(filepath, 'rb') as f:
            content = f.read()
            
        content_type = self._get_content_type(filename)
        return Response(content, 200, {'Content-Type': content_type})
        
    def _serve_public(self, request, filename):
        """Serve public files directly from the public folder."""
        base_dir = os.path.dirname(sys.modules[self.import_name].__file__)
        filepath = os.path.join(base_dir, self.public_folder, filename)
        
        if not os.path.exists(filepath) or not os.path.isfile(filepath):
            # File not found in public directory, try standard routing instead
            return None
        
        with open(filepath, 'rb') as f:
            content = f.read()
            
        content_type = self._get_content_type(filename)
        return Response(content, 200, {'Content-Type': content_type})
    
    def __call__(self, environ, start_response):
        """WSGI callable for the application."""
        request = Request(environ)
        
        # Trigger before_request hook
        if self.config['PLUGINS_ENABLED']:
            hook_results = hook.trigger('before_request', self, request)
            # Check if any hook returned a response
            for result in hook_results:
                if isinstance(result, Response):
                    # A hook returned a response, use it and skip normal processing
                    response = result
                    # Apply middleware post-processing
                    response = self.middleware_stack.process_response(request, response)
                    # Convert response to WSGI format and send
                    status, headers, body = response.to_wsgi()
                    start_response(status, headers)
                    return body
        
        # Apply middleware pre-processing
        request = self.middleware_stack.process_request(request)
        
        try:
            # Try to route the request
            handler, params = self.router.match_route(request.path, request.method)
            
            if handler:
                # Route matched, execute the handler with request and route params
                result = handler(request, **params)
                
                # Convert handler result to Response if it's not already
                if not isinstance(result, Response):
                    if isinstance(result, tuple) and len(result) == 2:
                        # Format: (body, status_code)
                        body, status_code = result
                        response = Response(body, status_code)
                    elif isinstance(result, (str, bytes)):
                        # String response
                        response = Response(result)
                    elif result is None:
                        # No content
                        response = Response('', 204)
                    else:
                        # Try to convert to JSON
                        response = Response.json(result)
                else:
                    response = result
            else:
                # No route matched
                response = self.error_handler.handle_error(404, request)
        
        except Exception as e:
            # Handle any exceptions
            response = self.error_handler.handle_error(e, request)
            # Trigger exception hooks
            if self.config['PLUGINS_ENABLED']:
                hook.trigger('request_exception', self, request, e)
        
        # Trigger after_request hook
        if self.config['PLUGINS_ENABLED']:
            hook_results = hook.trigger('after_request', self, request, response)
            # Check if any hook modified the response
            for result in hook_results:
                if isinstance(result, Response):
                    response = result
        
        # Apply middleware post-processing
        response = self.middleware_stack.process_response(request, response)
        
        # Convert response to WSGI format and send
        status, headers, body = response.to_wsgi()
        start_response(status, headers)
        return body
    
    def route(self, path, methods=None):
        """Route decorator to register handler functions."""
        methods = methods or ['GET']
        
        def decorator(handler):
            self.router.add_route(path, handler, methods)
            return handler
            
        return decorator
    
    def error_handler(self, code_or_exception):
        """Error handler decorator to register error handlers."""
        def decorator(handler):
            self.error_handler.register(code_or_exception, handler)
            return handler
            
        return decorator
    
    def render_template(self, template_name, **context):
        """Render a template with the given context."""
        return self.template_engine.render(template_name, **context)
    
    def use_middleware(self, middleware_class, *args, **kwargs):
        """Add middleware to the application."""
        middleware = middleware_class(*args, **kwargs) if callable(middleware_class) else middleware_class
        self.middleware_stack.add(middleware)
        return middleware
    
    def register_plugin(self, plugin_class):
        """
        Register a plugin with the application.
        
        Args:
            plugin_class: Plugin class to register
            
        Returns:
            The plugin instance
        """
        from .plugins import register_plugin
        plugin = register_plugin(plugin_class)
        if self.config['PLUGINS_ENABLED']:
            self.plugin_manager.enable_plugin(plugin.name)
        return plugin
    
    def enable_plugin(self, plugin_name):
        """
        Enable a plugin.
        
        Args:
            plugin_name: Name of the plugin to enable
            
        Returns:
            True if successful, False otherwise
        """
        return self.plugin_manager.enable_plugin(plugin_name)
    
    def disable_plugin(self, plugin_name):
        """
        Disable a plugin.
        
        Args:
            plugin_name: Name of the plugin to disable
            
        Returns:
            True if successful, False otherwise
        """
        return self.plugin_manager.disable_plugin(plugin_name)
    
    def get_enabled_plugins(self):
        """
        Get all enabled plugins.
        
        Returns:
            List of enabled plugin instances
        """
        return self.plugin_manager.get_enabled_plugins()
    
    def get_plugin_info(self, plugin_name):
        """
        Get detailed information about a plugin.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            Dictionary with plugin info or None if not found
        """
        return self.plugin_manager.get_plugin_info(plugin_name)
    
    def initialize_plugins(self):
        """Initialize all enabled plugins."""
        if self.config['PLUGINS_ENABLED']:
            self.plugin_manager.initialize_plugins()
            
    def mount(self, prefix, sub_app):
        """
        Mount a sub-application at a URL prefix.
        
        Args:
            prefix: URL prefix to mount the sub-app at
            sub_app: PyProApp instance to mount
            
        Returns:
            The sub-app instance
        """
        # TODO: Implement mounting logic
        pass
    
    def run(self, host='0.0.0.0', port=5000, debug=None):
        """Run the application with a simple WSGI server."""
        port = int(port)
        if debug is not None:
            self.config['DEBUG'] = debug
        
        if self.config['DEBUG']:
            logging.basicConfig(level=logging.DEBUG)
            
        # Initialize plugins
        if self.config['PLUGINS_ENABLED']:
            self.initialize_plugins()
            
        # Custom request handler to improve logging
        class CustomHandler(WSGIRequestHandler):
            def log_request(self, code='-', size='-'):
                if code == 200:
                    logging.info(f"{self.requestline} -> {code} {size}")
                else:
                    logging.warning(f"{self.requestline} -> {code} {size}")
        
        try:
            # Trigger application started event
            hook.trigger('application_started', self)
            
            print(f" * Running on http://{host}:{port}")
            print(" * Debug mode:", "on" if self.config['DEBUG'] else "off")
            if self.config['PLUGINS_ENABLED']:
                enabled_plugins = self.get_enabled_plugins()
                print(f" * Plugins: {len(enabled_plugins)} enabled")
            
            # Start the server
            httpd = make_server(host, port, self, handler_class=CustomHandler)
            
            # Set up clean shutdown on SIGINT
            def shutdown_server(signum, frame):
                print("\n * Shutting down...")
                # Trigger application stopping event
                hook.trigger('application_stopping', self)
                httpd.shutdown()
                sys.exit(0)
                
            signal.signal(signal.SIGINT, shutdown_server)
            
            # Serve until process is killed
            httpd.serve_forever()
            
        except socket.error as e:
            if e.errno == 98:  # Address already in use
                logging.error(f"Port {port} is already in use.")
            else:
                logging.error(f"Socket error: {e}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"Error starting server: {e}")
            sys.exit(1)