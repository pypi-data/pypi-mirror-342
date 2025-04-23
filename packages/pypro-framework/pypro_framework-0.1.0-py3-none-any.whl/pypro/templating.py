"""
Templating module for PyPro.

This module provides Jinja2 template integration with a fallback
to a simple string substitution engine when Jinja2 is not available.
"""

import os
import sys
import re
from typing import Dict, Any, Optional

try:
    import jinja2
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False


class TemplateEngine:
    """Template engine for rendering HTML templates."""
    
    def __init__(self, app=None):
        self.app = app
        self.template_dir = None
        self.jinja_env = None
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the template engine with an application."""
        self.app = app
        
        # Find template directory
        if app.import_name == '__main__':
            base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        else:
            base_dir = os.path.dirname(sys.modules[app.import_name].__file__)
            
        self.template_dir = os.path.join(base_dir, app.template_folder)
        
        # Setup Jinja2 if available
        if JINJA2_AVAILABLE:
            self.jinja_env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(self.template_dir),
                autoescape=jinja2.select_autoescape(['html', 'xml']),
                trim_blocks=True,
                lstrip_blocks=True
            )
            
            # Add global functions
            self.jinja_env.globals.update({
                'url_for': app.router.url_for if hasattr(app, 'router') else lambda x: x,
            })
    
    def render(self, template_name: str, **context) -> str:
        """
        Render a template with the given context variables.
        
        Args:
            template_name: Name of the template file
            **context: Variables to pass to the template
            
        Returns:
            Rendered template string
        """
        if not self.template_dir:
            raise RuntimeError("Template directory not set. Initialize with app first.")
            
        # Use Jinja2 if available
        if JINJA2_AVAILABLE and self.jinja_env:
            try:
                template = self.jinja_env.get_template(template_name)
                return template.render(**context)
            except jinja2.exceptions.TemplateNotFound:
                raise FileNotFoundError(f"Template '{template_name}' not found")
        
        # Fallback to simple template engine
        template_path = os.path.join(self.template_dir, template_name)
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template '{template_name}' not found")
            
        with open(template_path, 'r') as f:
            template_content = f.read()
            
        # Simple template substitution with {{ var }} syntax
        return self._simple_render(template_content, context)
    
    def _simple_render(self, template_content: str, context: Dict[str, Any]) -> str:
        """
        Simple template rendering engine for when Jinja2 is not available.
        
        Handles basic {{ var }} substitutions.
        """
        def replace_var(match):
            var_name = match.group(1).strip()
            # Handle nested attributes with dot notation
            if '.' in var_name:
                parts = var_name.split('.')
                value = context
                for part in parts:
                    if isinstance(value, dict) and part in value:
                        value = value[part]
                    elif hasattr(value, part):
                        value = getattr(value, part)
                    else:
                        return match.group(0)  # Keep original if not found
                return str(value)
            
            # Simple variable lookup
            return str(context.get(var_name, match.group(0)))
        
        # Replace {{ var }} patterns
        result = re.sub(r'{{(.*?)}}', replace_var, template_content)
        return result


def render_template(template_name: str, **context) -> str:
    """
    Global function to render a template.
    
    This should be replaced at runtime with app.render_template.
    """
    raise RuntimeError(
        "render_template() called before app initialization. "
        "This function should be called within an application context."
    )
