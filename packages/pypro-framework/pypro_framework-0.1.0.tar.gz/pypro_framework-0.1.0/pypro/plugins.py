"""
Plugin system for PyPro.

This module provides a comprehensive plugin system that allows third-party
packages to extend PyPro's functionality through various extension points.

The plugin system includes:
- Plugin discovery and registration
- Plugin lifecycle management (load, enable, disable)
- Event hooks for application lifecycle events
- Configuration management
- Plugin dependency management
- API versioning
"""

import os
import sys
import json
import logging
import importlib
import pkgutil
import inspect
from typing import Dict, List, Callable, Any, Optional, Type, Set, Tuple, Union
from importlib.metadata import version as pkg_version
from importlib.metadata import PackageNotFoundError

# Registry of installed plugins
_plugins = {}  # name -> plugin instance

# Registry of hooks by event name
_hooks = {}  # event_name -> list of callbacks

# API Version
API_VERSION = "1.0.0"

class PluginDependencyError(Exception):
    """Exception raised when a plugin dependency is not satisfied."""
    pass

class PluginAPIVersionError(Exception):
    """Exception raised when a plugin is not compatible with current API version."""
    pass

class PluginHookRegistry:
    """Registry for plugin hooks."""
    
    @staticmethod
    def register(event_name: str, callback: Callable, priority: int = 0):
        """
        Register a callback for an event.
        
        Args:
            event_name: Name of the event to register for
            callback: Function to call when the event is triggered
            priority: Priority of this callback (higher is called first)
        """
        if event_name not in _hooks:
            _hooks[event_name] = []
        
        _hooks[event_name].append((callback, priority))
        # Sort by priority (highest first)
        _hooks[event_name].sort(key=lambda x: x[1], reverse=True)
    
    @staticmethod
    def trigger(event_name: str, *args, **kwargs) -> List[Any]:
        """
        Trigger an event, calling all registered callbacks.
        
        Args:
            event_name: Name of the event to trigger
            *args: Arguments to pass to callbacks
            **kwargs: Keyword arguments to pass to callbacks
            
        Returns:
            List of return values from callbacks
        """
        results = []
        
        if event_name in _hooks:
            for callback, _ in _hooks[event_name]:
                try:
                    result = callback(*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    logging.error(f"Error in hook {callback.__name__} for event {event_name}: {e}")
        
        return results

# Convenience alias
hook = PluginHookRegistry

def pkg_version_lt(v1: str, v2: str) -> bool:
    """
    Compare two version strings.
    
    Args:
        v1: First version string
        v2: Second version string
        
    Returns:
        True if v1 < v2, False otherwise
    """
    def normalize(v):
        return [int(x) for x in v.split(".")]
    
    return normalize(v1) < normalize(v2)

class Plugin:
    """Base class for all PyPro plugins."""
    
    name = "base_plugin"
    version = "0.1.0"
    description = "Base plugin class for PyPro"
    author = ""
    license = ""
    homepage = ""
    api_version = API_VERSION
    
    # Dependencies format: {plugin_name: min_version}
    dependencies = {}
    
    def __init__(self):
        self.app = None
        self.config = {}
        self.enabled = False
        self._hooks = []  # List of registered hooks for cleanup
    
    def init_app(self, app):
        """
        Initialize the plugin with an application.
        
        Args:
            app: PyProApp instance
        """
        self.app = app
        self.load_config()
        
        # Register hooks
        self.register_hooks()
        
        # Trigger initialization event
        hook.trigger('plugin_initialized', self)
    
    def register_routes(self):
        """Register routes with the application."""
        pass
    
    def register_commands(self):
        """Register CLI commands with the application."""
        pass
    
    def register_middleware(self):
        """Register middleware with the application."""
        pass
    
    def register_templates(self):
        """Register template helpers with the application."""
        pass
    
    def register_hooks(self):
        """Register hooks for the plugin."""
        pass
    
    def on_hook(self, event_name: str, priority: int = 0):
        """
        Decorator to register a method as a hook handler.
        
        Args:
            event_name: Name of the event to handle
            priority: Priority of this handler (higher is called first)
            
        Returns:
            Decorator function
        """
        def decorator(func):
            hook.register(event_name, func, priority)
            self._hooks.append((event_name, func))
            return func
        return decorator
    
    def load_config(self):
        """Load plugin configuration from file or environment."""
        # Default config file is in the app's config directory
        if self.app and hasattr(self.app, 'config'):
            # Try to get plugin-specific config
            plugin_config = self.app.config.get(f'PLUGIN_{self.name.upper()}', {})
            self.config.update(plugin_config)
        
        # Load from environment variables
        prefix = f"PYPRO_PLUGIN_{self.name.upper()}_"
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):]
                self.config[config_key] = value
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key is not found
            
        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)
    
    def validate_dependencies(self):
        """
        Validate that all dependencies are satisfied.
        
        Raises:
            PluginDependencyError: If a dependency is not satisfied
        """
        for plugin_name, min_version in self.dependencies.items():
            # Check if plugin is installed
            if plugin_name not in _plugins:
                raise PluginDependencyError(
                    f"Missing dependency: {plugin_name} (required by {self.name})"
                )
            
            # Check version
            plugin = _plugins[plugin_name]
            if pkg_version_lt(plugin.version, min_version):
                raise PluginDependencyError(
                    f"Incompatible plugin version: {plugin_name} {plugin.version} "
                    f"(required: >={min_version}, by {self.name})"
                )
    
    def validate_api_version(self):
        """
        Validate that the plugin is compatible with current API version.
        
        Raises:
            PluginAPIVersionError: If the plugin is not compatible
        """
        # Simple version check for now
        if self.api_version != API_VERSION:
            raise PluginAPIVersionError(
                f"Plugin {self.name} uses API version {self.api_version}, "
                f"but current API version is {API_VERSION}"
            )
    
    def enable(self):
        """
        Enable the plugin.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.validate_dependencies()
            self.validate_api_version()
            self.enabled = True
            hook.trigger('plugin_enabled', self)
            return True
        except (PluginDependencyError, PluginAPIVersionError) as e:
            logging.error(f"Error enabling plugin {self.name}: {e}")
            return False
    
    def disable(self):
        """
        Disable the plugin.
        
        Returns:
            True if successful, False otherwise
        """
        if self.enabled:
            self.enabled = False
            hook.trigger('plugin_disabled', self)
            return True
        return False
    
    def uninstall(self):
        """
        Uninstall the plugin, cleaning up any resources.
        
        Returns:
            True if successful, False otherwise
        """
        if self.enabled:
            self.disable()
        
        # Remove all registered hooks
        for event_name, callback in self._hooks:
            if event_name in _hooks:
                _hooks[event_name] = [(cb, prio) for cb, prio in _hooks[event_name] 
                                     if cb != callback]
        
        hook.trigger('plugin_uninstalled', self)
        return True


def register_plugin(plugin_class: Type[Plugin]):
    """
    Register a plugin with PyPro.
    
    Args:
        plugin_class: Plugin class to register
        
    Returns:
        The plugin instance
    """
    plugin = plugin_class()
    _plugins[plugin.name] = plugin
    return plugin


def get_plugins() -> List[Plugin]:
    """
    Get all registered plugins.
    
    Returns:
        List of plugin instances
    """
    return list(_plugins.values())


def discover_plugins():
    """
    Discover and register all PyPro plugins.
    
    Plugins should be installed packages with a name starting with
    'pypro-' or 'pypro_' and implementing the Plugin interface.
    """
    for item in pkgutil.iter_modules():
        # Check if module name starts with pypro- or pypro_
        if item.name.startswith("pypro-") or item.name.startswith("pypro_"):
            try:
                # Import the module
                module = importlib.import_module(item.name)
                
                # Look for Plugin subclasses
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    
                    # Check if it's a Plugin subclass
                    if (isinstance(attr, type) and 
                            issubclass(attr, Plugin) and 
                            attr is not Plugin):
                        register_plugin(attr)
                        logging.info(f"Registered plugin: {attr.name} v{attr.version}")
            except ImportError as e:
                logging.warning(f"Error importing plugin {item.name}: {e}")


class PluginManager:
    """
    Manager for PyPro plugins.
    
    This class provides methods for installing, enabling, disabling,
    and managing plugins.
    """
    
    def __init__(self, app=None):
        self.app = app
        self.enabled_plugins = set()
        
    def init_app(self, app):
        """Initialize with an application."""
        self.app = app
        
    def load_plugin(self, plugin_name):
        """
        Load a plugin by name.
        
        Args:
            plugin_name: Name of the plugin to load
            
        Returns:
            The loaded plugin or None if not found
        """
        try:
            # Try to import the module
            module_name = plugin_name
            if not (module_name.startswith("pypro-") or module_name.startswith("pypro_")):
                module_name = f"pypro_{plugin_name}"
                
            module = importlib.import_module(module_name)
            
            # Find the plugin class
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                
                # Check if it's a Plugin subclass
                if (isinstance(attr, type) and 
                        issubclass(attr, Plugin) and 
                        attr is not Plugin):
                    plugin = register_plugin(attr)
                    self.enabled_plugins.add(plugin.name)
                    return plugin
                    
            logging.warning(f"No plugin class found in module {module_name}")
            return None
            
        except ImportError as e:
            logging.error(f"Error loading plugin {plugin_name}: {e}")
            return None
            
    def enable_plugin(self, plugin_name):
        """
        Enable a plugin.
        
        Args:
            plugin_name: Name of the plugin to enable
            
        Returns:
            True if successful, False otherwise
        """
        # Check if plugin is already loaded
        if plugin_name in _plugins:
            plugin = _plugins[plugin_name]
            if plugin.enable():
                self.enabled_plugins.add(plugin_name)
                return True
            return False
                
        # Try to load the plugin
        plugin = self.load_plugin(plugin_name)
        if plugin and plugin.enable():
            self.enabled_plugins.add(plugin_name)
            return True
        return False
        
    def disable_plugin(self, plugin_name):
        """
        Disable a plugin.
        
        Args:
            plugin_name: Name of the plugin to disable
            
        Returns:
            True if successful, False otherwise
        """
        if plugin_name in self.enabled_plugins and plugin_name in _plugins:
            plugin = _plugins[plugin_name]
            if plugin.disable():
                self.enabled_plugins.remove(plugin_name)
                return True
        return False
        
    def get_enabled_plugins(self):
        """
        Get all enabled plugins.
        
        Returns:
            List of enabled plugin instances
        """
        return [_plugins[name] for name in self.enabled_plugins if name in _plugins]
        
    def initialize_plugins(self):
        """Initialize all enabled plugins with the application."""
        if not self.app:
            raise ValueError("PluginManager not initialized with an app")
            
        for plugin in self.get_enabled_plugins():
            try:
                plugin.init_app(self.app)
                plugin.register_routes()
                plugin.register_commands()
                plugin.register_middleware()
                plugin.register_templates()
                hook.trigger('plugin_initialized', plugin)
            except Exception as e:
                logging.error(f"Error initializing plugin {plugin.name}: {e}")
    
    def uninstall_plugin(self, plugin_name):
        """
        Uninstall a plugin.
        
        Args:
            plugin_name: Name of the plugin to uninstall
            
        Returns:
            True if successful, False otherwise
        """
        if plugin_name in _plugins:
            plugin = _plugins[plugin_name]
            
            # Disable the plugin if it's enabled
            if plugin_name in self.enabled_plugins:
                self.disable_plugin(plugin_name)
            
            # Call the plugin's uninstall method
            try:
                if plugin.uninstall():
                    # Remove from registry
                    del _plugins[plugin_name]
                    return True
            except Exception as e:
                logging.error(f"Error uninstalling plugin {plugin_name}: {e}")
        
        return False
    
    def list_available_plugins(self):
        """
        List all available plugins.
        
        Returns:
            List of dictionaries with plugin info
        """
        plugins_info = []
        
        for name, plugin in _plugins.items():
            plugins_info.append({
                'name': name,
                'version': plugin.version,
                'description': plugin.description,
                'author': plugin.author,
                'enabled': name in self.enabled_plugins
            })
            
        return plugins_info
    
    def get_plugin_info(self, plugin_name):
        """
        Get detailed information about a plugin.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            Dictionary with plugin info or None if not found
        """
        if plugin_name in _plugins:
            plugin = _plugins[plugin_name]
            return {
                'name': plugin.name,
                'version': plugin.version,
                'description': plugin.description,
                'author': plugin.author,
                'license': plugin.license,
                'homepage': plugin.homepage,
                'api_version': plugin.api_version,
                'dependencies': plugin.dependencies,
                'enabled': plugin_name in self.enabled_plugins,
                'config': plugin.config
            }
        
        return None
