"""
Utility functions for PyPro applications.
"""

import os
import sys
import json
import logging
import uuid
import time
import inspect
import importlib.util
from typing import Any, Dict, List, Optional, Callable, Union, Tuple, Set

# HTTP status codes
HTTP_STATUSES = {
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    204: 'No Content',
    300: 'Multiple Choices',
    301: 'Moved Permanently',
    302: 'Found',
    304: 'Not Modified',
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    409: 'Conflict',
    422: 'Unprocessable Entity',
    429: 'Too Many Requests',
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable'
}


def load_module_from_path(path: str) -> Optional[Any]:
    """
    Load a Python module from a file path.
    
    Args:
        path: Path to the Python file
        
    Returns:
        Module object if successful, None otherwise
    """
    try:
        module_name = os.path.basename(path).replace('.py', '').replace('.', '_')
        spec = importlib.util.spec_from_file_location(module_name, path)
        if not spec or not spec.loader:
            return None
            
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except (ImportError, SyntaxError) as e:
        logging.error(f"Error loading module from {path}: {e}")
        return None


def find_modules_in_directory(directory: str, exclude: Optional[Set[str]] = None) -> List[Tuple[str, Any]]:
    """
    Find all Python modules in a directory.
    
    Args:
        directory: Directory path to search
        exclude: Set of filenames to exclude
        
    Returns:
        List of (filename, module) tuples
    """
    if exclude is None:
        exclude = set()
        
    modules = []
    
    if not os.path.exists(directory) or not os.path.isdir(directory):
        return modules
        
    for filename in os.listdir(directory):
        if filename.endswith('.py') and filename not in exclude:
            filepath = os.path.join(directory, filename)
            module = load_module_from_path(filepath)
            if module:
                modules.append((filename, module))
                
    return modules


def get_callable_attributes(obj: Any) -> List[Tuple[str, Callable]]:
    """
    Get all callable attributes of an object.
    
    Args:
        obj: Object to inspect
        
    Returns:
        List of (name, callable) tuples
    """
    result = []
    for name in dir(obj):
        if name.startswith('_'):
            continue
            
        attr = getattr(obj, name)
        if callable(attr):
            result.append((name, attr))
            
    return result


def generate_id() -> str:
    """
    Generate a unique ID.
    
    Returns:
        String ID
    """
    return str(uuid.uuid4())


def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """
    Merge two dictionaries recursively.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary (values override dict1)
        
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # Recursively merge nested dictionaries
            result[key] = merge_dicts(result[key], value)
        else:
            # Override or add values
            result[key] = value
            
    return result


def to_list(value: Union[Any, List[Any]]) -> List[Any]:
    """
    Convert a value to a list if it's not already.
    
    Args:
        value: Value to convert
        
    Returns:
        List containing the value, or the value if already a list
    """
    if isinstance(value, list):
        return value
    return [value]


def parse_query_string(query_string: str) -> Dict[str, Union[str, List[str]]]:
    """
    Parse a query string into a dictionary.
    
    Args:
        query_string: Query string (without leading '?')
        
    Returns:
        Dictionary of parameter names to values
    """
    if not query_string:
        return {}
        
    result = {}
    for param in query_string.split('&'):
        if '=' in param:
            key, value = param.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            if key in result:
                if isinstance(result[key], list):
                    result[key].append(value)
                else:
                    result[key] = [result[key], value]
            else:
                result[key] = value
        else:
            result[param.strip()] = True
            
    return result


def format_exception(e: Exception) -> str:
    """
    Format an exception as a string.
    
    Args:
        e: Exception object
        
    Returns:
        Formatted exception string
    """
    import traceback
    tb_lines = traceback.format_exception(type(e), e, e.__traceback__)
    return ''.join(tb_lines)


def timed_lru_cache(seconds: int, maxsize: int = 128):
    """
    Decorator that provides a timed LRU cache.
    
    Args:
        seconds: Time in seconds to cache results
        maxsize: Maximum cache size
        
    Returns:
        Decorator function
    """
    def decorator(func):
        cache = {}
        timestamps = {}
        
        def wrapper(*args, **kwargs):
            key = str((args, frozenset(kwargs.items())))
            now = time.time()
            
            # Remove any expired entries
            for k in list(cache.keys()):
                if now - timestamps[k] > seconds:
                    del cache[k]
                    del timestamps[k]
            
            # Limit cache size if needed
            if len(cache) >= maxsize:
                oldest_key = min(timestamps.items(), key=lambda x: x[1])[0]
                if oldest_key in cache:
                    del cache[oldest_key]
                    del timestamps[oldest_key]
            
            # Return cached value if available
            if key in cache:
                return cache[key]
            
            # Calculate and cache the result
            result = func(*args, **kwargs)
            cache[key] = result
            timestamps[key] = now
            return result
        
        return wrapper
    
    return decorator


def load_json_file(path: str, default: Any = None) -> Any:
    """
    Load JSON data from a file.
    
    Args:
        path: Path to the JSON file
        default: Default value to return if file is missing or invalid
        
    Returns:
        Parsed JSON data or the default value
    """
    try:
        if not os.path.exists(path):
            return default
            
        with open(path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def save_json_file(path: str, data: Any, indent: int = 2) -> bool:
    """
    Save data to a JSON file.
    
    Args:
        path: Path to the JSON file
        data: Data to save
        indent: JSON indentation level
        
    Returns:
        True if successful, False otherwise
    """
    try:
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(path, 'w') as f:
            json.dump(data, f, indent=indent)
        return True
    except OSError as e:
        logging.error(f"Error saving JSON file: {e}")
        return False
