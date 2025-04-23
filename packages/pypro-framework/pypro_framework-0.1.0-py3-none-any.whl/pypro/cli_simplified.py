"""
Command-line interface for PyPro.

This module provides a CLI tool for running PyPro applications and
performing other tasks like database migrations.
"""

import os
import sys
import argparse
import logging
import importlib.util
from typing import List, Optional, Dict, Any

from . import __version__
from .app import PyProApp
from .utils import load_module_from_path
from .plugins import discover_plugins


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Args:
        args: Command-line arguments
        
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        prog='pyp',
        description='PyPro web framework command-line tool'
    )
    
    # Add command subparsers
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # run command
    run_parser = subparsers.add_parser('run', help='Run a PyPro application')
    run_parser.add_argument(
        'file', 
        help='Path to the Python module containing a PyPro app'
    )
    run_parser.add_argument(
        '--host', '-H',
        default='0.0.0.0',
        help='Host to bind to (default: 0.0.0.0)'
    )
    run_parser.add_argument(
        '--port', '-p',
        type=int,
        default=5000,
        help='Port to bind to (default: 5000)'
    )
    run_parser.add_argument(
        '--debug', '-d',
        action='store_true',
        help='Enable debug mode'
    )
    
    # new command
    new_parser = subparsers.add_parser('new', help='Create a new PyPro project')
    new_parser.add_argument(
        'name',
        help='Name of the project'
    )
    new_parser.add_argument(
        '--minimal', '-m',
        action='store_true',
        help='Create a minimal project'
    )
    new_parser.add_argument(
        '--template', '-t',
        choices=['basic', 'api', 'mvc', 'spa'],
        default='basic',
        help='Project template to use (default: basic)'
    )
    
    # create-app command
    create_app_parser = subparsers.add_parser('create-app', help='Create a new app module within a project')
    create_app_parser.add_argument(
        'name',
        help='Name of the app module'
    )
    create_app_parser.add_argument(
        '--project-dir', '-p',
        default='.',
        help='Path to the project directory (default: current directory)'
    )
    
    # routes command
    routes_parser = subparsers.add_parser('routes', help='List all routes in the application')
    routes_parser.add_argument(
        'file',
        help='Path to the Python module containing a PyPro app'
    )
    
    # version command
    version_parser = subparsers.add_parser('version', help='Show the PyPro version')
    
    # Add a shortcut for --version
    parser.add_argument('--version', action='store_true', help='Show the PyPro version')
    
    # Parse arguments
    return parser.parse_args(args)


def load_app_from_file(file_path: str) -> Optional[PyProApp]:
    """
    Load a PyPro application from a file.
    
    Args:
        file_path: Path to the Python module containing a PyPro app
        
    Returns:
        PyProApp instance if successful, None otherwise
    """
    # Ensure the file exists
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return None
        
    # Add the directory to sys.path
    file_dir = os.path.dirname(os.path.abspath(file_path))
    if file_dir not in sys.path:
        sys.path.insert(0, file_dir)
        
    # Load the module
    module = load_module_from_path(file_path)
    if not module:
        return None
        
    # Find the PyProApp instance
    app = None
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, PyProApp):
            app = attr
            break
            
    if not app:
        logging.error(f"No PyProApp instance found in {file_path}")
        return None
        
    return app


def run_command(args: argparse.Namespace):
    """
    Run a PyPro application.
    
    Args:
        args: Command-line arguments
    """
    app = load_app_from_file(args.file)
    if not app:
        return 1
        
    try:
        app.run(host=args.host, port=args.port, debug=args.debug)
        return 0
    except Exception as e:
        logging.error(f"Error running application: {e}")
        return 1


def new_command(args: argparse.Namespace):
    """
    Create a new PyPro project.
    
    Args:
        args: Command-line arguments
    """
    project_path = os.path.abspath(args.name)
    project_name = os.path.basename(project_path)
    
    # Ensure the directory doesn't exist
    if os.path.exists(project_path):
        logging.error(f"Directory already exists: {project_path}")
        return 1
        
    # Create the project directory
    os.makedirs(project_path)
    
    # Create app structure
    if args.minimal:
        # Create a minimal project
        app_py_content = """from pypro import PyProApp, render_template

app = PyProApp(__name__, template_folder='templates', static_folder='static', public_folder='public')
app.config['DEBUG'] = True

@app.route('/')
def index(request):
    return render_template('index.html', title='Welcome to PyPro')

if __name__ == '__main__':
    app.run(debug=True)
"""
        with open(os.path.join(project_path, 'app.py'), 'w') as f:
            f.write(app_py_content)
        
        # Create templates directory
        os.makedirs(os.path.join(project_path, 'templates'))
        
        # Create index template
        index_html_content = """<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <h1>{{ title }}</h1>
    <p>Congratulations! Your PyPro application is running.</p>
    <p>
        <a href="/public/docs/guide.html">Read the docs</a>
    </p>
</body>
</html>
"""
        with open(os.path.join(project_path, 'templates', 'index.html'), 'w') as f:
            f.write(index_html_content)
        
        # Create static directories
        os.makedirs(os.path.join(project_path, 'static', 'css'))
        
        # Create CSS file
        css_content = """body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}
h1 {
    color: #333;
}
a {
    color: #0066cc;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
"""
        with open(os.path.join(project_path, 'static', 'css', 'style.css'), 'w') as f:
            f.write(css_content)
        
        # Create public directory
        os.makedirs(os.path.join(project_path, 'public', 'docs'))
        
        # Create a documentation file
        guide_html_content = """<!DOCTYPE html>
<html>
<head>
    <title>PyPro Guide</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2 {
            color: #333;
        }
        code {
            background-color: #f5f5f5;
            padding: 2px 4px;
            border-radius: 3px;
        }
        pre {
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <h1>PyPro Framework Guide</h1>
    <p>
        This is a minimal PyPro project. Here's how to get started:
    </p>
    <h2>Project Structure</h2>
    <pre>
- app.py          # Main application file
- templates/      # HTML templates
- static/         # CSS, JS, and other static files
- public/         # Publicly accessible files
    </pre>
    
    <h2>Adding Routes</h2>
    <p>
        To add a new route, open <code>app.py</code> and add a new route handler:
    </p>
    <pre>
@app.route('/hello/<name>')
def hello(request, name):
    return f"Hello, {name}!"
    </pre>
    
    <p><a href="/">Back to home</a></p>
</body>
</html>
"""
        with open(os.path.join(project_path, 'public', 'docs', 'guide.html'), 'w') as f:
            f.write(guide_html_content)
    else:
        # Create a basic project with app directory
        app_dir = os.path.join(project_path, 'app')
        os.makedirs(app_dir)
        
        # Create template directories
        templates_dir = os.path.join(project_path, 'templates')
        os.makedirs(templates_dir)
        
        # Create static directories
        static_dir = os.path.join(project_path, 'static')
        os.makedirs(os.path.join(static_dir, 'css'))
        os.makedirs(os.path.join(static_dir, 'js'))
        
        # Create public directory
        public_dir = os.path.join(project_path, 'public')
        os.makedirs(public_dir)
        
        # Create app/__init__.py
        init_py_content = f"""from pypro import PyProApp, Database, SessionMiddleware, CSRFMiddleware

app = PyProApp(__name__, 
               template_folder='../templates',
               static_folder='../static',
               public_folder='../public')

# Configure the app
app.config.update({{
    'DEBUG': True,
    'PROJECT_NAME': '{project_name}',
}})

# Initialize database
db = Database(app)

# Add middleware
app.use_middleware(SessionMiddleware, app)
app.use_middleware(CSRFMiddleware, app)

# Import routes
from . import routes
"""
        with open(os.path.join(app_dir, '__init__.py'), 'w') as f:
            f.write(init_py_content)
        
        # Create app/routes.py
        routes_py_content = """from . import app
from pypro import render_template

@app.route('/')
def index(request):
    return render_template('index.html', title='Welcome to PyPro')

@app.route('/about')
def about(request):
    return render_template('about.html', title='About')

@app.route('/api/hello/<name>')
def api_hello(request, name):
    return {'message': f'Hello, {name}!'}
"""
        with open(os.path.join(app_dir, 'routes.py'), 'w') as f:
            f.write(routes_py_content)
        
        # Create main.py
        main_py_content = """from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
"""
        with open(os.path.join(project_path, 'main.py'), 'w') as f:
            f.write(main_py_content)
        
        # Create templates/index.html
        index_html_content = """<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <h1>{{ title }}</h1>
    <p>Welcome to your PyPro application!</p>
    <nav>
        <a href="/">Home</a> | 
        <a href="/about">About</a>
    </nav>
    <p>
        <a href="/api/hello/world">Try the API</a>
    </p>
</body>
</html>
"""
        with open(os.path.join(templates_dir, 'index.html'), 'w') as f:
            f.write(index_html_content)
        
        # Create templates/about.html
        about_html_content = """<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <h1>{{ title }}</h1>
    <p>This is a PyPro application with batteries included.</p>
    <nav>
        <a href="/">Home</a> | 
        <a href="/about">About</a>
    </nav>
</body>
</html>
"""
        with open(os.path.join(templates_dir, 'about.html'), 'w') as f:
            f.write(about_html_content)
        
        # Create static/css/style.css
        css_content = """body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}
h1 {
    color: #333;
}
a {
    color: #0066cc;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
nav {
    margin: 20px 0;
    padding: 10px;
    background-color: #f5f5f5;
    border-radius: 5px;
}
"""
        with open(os.path.join(static_dir, 'css', 'style.css'), 'w') as f:
            f.write(css_content)
    
    print(f"✅ Successfully created a new PyPro project in {project_path}")
    if args.minimal:
        print("\nTo run the application:")
        print(f"cd {project_path}")
        print("python app.py")
    else:
        print("\nTo run the application:")
        print(f"cd {project_path}")
        print("python main.py")
    
    return 0


def create_app_command(args: argparse.Namespace):
    """
    Create a new app module within a PyPro project.
    
    Args:
        args: Command-line arguments
    """
    project_dir = os.path.abspath(args.project_dir)
    app_name = args.name
    app_dir = os.path.join(project_dir, app_name)
    
    # Ensure the project directory exists
    if not os.path.exists(project_dir):
        logging.error(f"Project directory not found: {project_dir}")
        return 1
        
    # Ensure the app directory doesn't exist
    if os.path.exists(app_dir):
        logging.error(f"App directory already exists: {app_dir}")
        return 1
        
    # Create the app directory
    os.makedirs(app_dir)
    
    # Create __init__.py
    init_py_content = f'''"""Module {app_name} for the PyPro application."""

from pypro import PyProApp

# Create a sub-app
app = PyProApp(__name__)

# Import routes
from . import routes
'''
    with open(os.path.join(app_dir, '__init__.py'), 'w') as f:
        f.write(init_py_content)
    
    # Create routes.py
    routes_py_content = f'''"""Routes for the {app_name} module."""

from . import app
from pypro import render_template

@app.route('/')
def index(request):
    """Handle the {app_name} index page."""
    return render_template('{app_name}/index.html', title='{app_name.title()}')

@app.route('/details')
def details(request):
    """Handle the {app_name} details page."""
    return render_template('{app_name}/details.html', title='{app_name.title()} Details')
'''
    with open(os.path.join(app_dir, 'routes.py'), 'w') as f:
        f.write(routes_py_content)
    
    # Create templates directory
    templates_dir = os.path.join(project_dir, 'templates', app_name)
    os.makedirs(templates_dir, exist_ok=True)
    
    # Create index.html
    index_html_content = f"""
{{% extends "base.html" if os.path.exists(os.path.join(project_dir, 'templates', 'base.html')) else "" %}}

{{% block content %}}
<div class="container mt-4">
    <h1>{{{{ title }}}}</h1>
    <p class="lead">Welcome to the {app_name} module!</p>
    
    <div class="card mt-4">
        <div class="card-body">
            <h5 class="card-title">{app_name.title()} Module</h5>
            <p class="card-text">
                This is a sub-application module created with the PyPro CLI.
            </p>
            <a href="/{app_name}/details" class="btn btn-primary">View Details</a>
        </div>
    </div>
</div>
{{% endblock %}}
"""
    with open(os.path.join(templates_dir, 'index.html'), 'w') as f:
        f.write(index_html_content)
    
    # Create details.html
    details_html_content = f"""
{{% extends "base.html" if os.path.exists(os.path.join(project_dir, 'templates', 'base.html')) else "" %}}

{{% block content %}}
<div class="container mt-4">
    <h1>{{{{ title }}}}</h1>
    <p class="lead">Details about the {app_name} module.</p>
    
    <div class="card mt-4">
        <div class="card-body">
            <h5 class="card-title">Module Structure</h5>
            <p class="card-text">
                The {app_name} module includes:
            </p>
            <ul>
                <li><code>__init__.py</code>: Module initialization</li>
                <li><code>routes.py</code>: URL routes</li>
            </ul>
        </div>
    </div>
    
    <a href="/{app_name}" class="btn btn-primary mt-3">Back to {app_name.title()}</a>
</div>
{{% endblock %}}
"""
    with open(os.path.join(templates_dir, 'details.html'), 'w') as f:
        f.write(details_html_content)
    
    print(f"\n✅ Successfully created a new app module '{app_name}' in {app_dir}")
    print("\nDirectory structure:")
    print(f"- {app_name}/")
    print(f"  - __init__.py")
    print(f"  - routes.py")
    print(f"- templates/{app_name}/")
    print(f"  - index.html")
    print(f"  - details.html")
    
    print(f"\nTo use this module, import and mount it in your main application:")
    print(f"from {app_name} import app as {app_name}_app")
    print(f"app.mount('/{app_name}', {app_name}_app)")
    
    return 0


def routes_command(args: argparse.Namespace):
    """
    List all routes in the application.
    
    Args:
        args: Command-line arguments
    """
    app = load_app_from_file(args.file)
    if not app:
        return 1
        
    # Get routes from the app
    routes = app.router.routes
    
    if not routes:
        print("No routes found in the application.")
        return 0
        
    # Print routes in a table format
    print(f"{'Route Path':<40} {'Methods':<20} {'Endpoint':<30}")
    print(f"{'-' * 40} {'-' * 20} {'-' * 30}")
    
    for route in routes:
        path = route['path']
        methods = ', '.join(route['methods'])
        endpoint = route['endpoint']
        
        print(f"{path:<40} {methods:<20} {endpoint:<30}")
        
    return 0


def version_command(args: argparse.Namespace):
    """
    Show the PyPro version.
    
    Args:
        args: Command-line arguments
    """
    print(f"PyPro v{__version__}")
    return 0


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the CLI.
    
    Args:
        args: Command-line arguments
        
    Returns:
        Exit code
    """
    # Parse arguments
    parsed_args = parse_args(args)
    
    # Check if --version flag was used
    if hasattr(parsed_args, 'version') and parsed_args.version:
        return version_command(parsed_args)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(message)s'
    )
    
    # Discover plugins
    discover_plugins()
    
    # Handle commands
    if parsed_args.command == 'run':
        return run_command(parsed_args)
    elif parsed_args.command == 'new':
        return new_command(parsed_args)
    elif parsed_args.command == 'create-app':
        return create_app_command(parsed_args)
    elif parsed_args.command == 'routes':
        return routes_command(parsed_args)
    elif parsed_args.command == 'version':
        return version_command(parsed_args)
    elif not parsed_args.command:
        # No command specified, show help
        print("PyPro CLI tool")
        print(f"Version: {__version__}")
        print("\nUse 'pyp --help' to see available commands")
        return 0
    else:
        logging.error(f"Unknown command: {parsed_args.command}")
        return 1


if __name__ == '__main__':
    sys.exit(main())