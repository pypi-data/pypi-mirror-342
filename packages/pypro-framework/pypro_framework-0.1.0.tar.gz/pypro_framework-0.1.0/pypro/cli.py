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
        help='Path to the .pyp file or Python module'
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
    
    # db command
    db_parser = subparsers.add_parser('db', help='Database operations')
    db_subparsers = db_parser.add_subparsers(dest='db_command', help='Database command')
    
    # db init command
    db_init_parser = db_subparsers.add_parser('init', help='Initialize database')
    db_init_parser.add_argument(
        'file',
        help='Path to the .pyp file or Python module'
    )
    
    # db migrate command
    db_migrate_parser = db_subparsers.add_parser('migrate', help='Create a new migration')
    db_migrate_parser.add_argument(
        'file',
        help='Path to the .pyp file or Python module'
    )
    db_migrate_parser.add_argument(
        'name',
        help='Name of the migration'
    )
    
    # db upgrade command
    db_upgrade_parser = db_subparsers.add_parser('upgrade', help='Apply migrations')
    db_upgrade_parser.add_argument(
        'file',
        help='Path to the .pyp file or Python module'
    )
    db_upgrade_parser.add_argument(
        '--target', '-t',
        help='Target migration (default: latest)'
    )
    
    # db downgrade command
    db_downgrade_parser = db_subparsers.add_parser('downgrade', help='Roll back migrations')
    db_downgrade_parser.add_argument(
        'file',
        help='Path to the .pyp file or Python module'
    )
    db_downgrade_parser.add_argument(
        '--steps', '-s',
        type=int,
        default=1,
        help='Number of migrations to roll back (default: 1)'
    )
    
    # shell command
    shell_parser = subparsers.add_parser('shell', help='Run a Python shell with PyPro environment')
    shell_parser.add_argument(
        'file',
        nargs='?',
        help='Path to the .pyp file or Python module'
    )
    
    # routes command
    routes_parser = subparsers.add_parser('routes', help='List all routes in the application')
    routes_parser.add_argument(
        'file',
        help='Path to the .pyp file or Python module'
    )
    
    # Parse arguments
    return parser.parse_args(args)


def load_app_from_file(file_path: str) -> Optional[PyProApp]:
    """
    Load a PyPro application from a file.
    
    Args:
        file_path: Path to the .pyp file or Python module
        
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
    
    if args.minimal:
        # Create a minimal project
        with open(os.path.join(project_path, 'app.py'), 'w') as f:
            f.write("""from pypro import PyProApp, render_template

app = PyProApp(__name__, template_folder='templates', static_folder='static', public_folder='public')
app.config['DEBUG'] = True

@app.route('/')
def index(request):
    return render_template('index.html', title='Welcome to PyPro')

if __name__ == '__main__':
    app.run(debug=True)
""")
        
        # Create templates directory
        os.makedirs(os.path.join(project_path, 'templates'))
        
        # Create index template
        with open(os.path.join(project_path, 'templates', 'index.html'), 'w') as f:
            f.write("""<!DOCTYPE html>
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
""")
        
        # Create static directories
        os.makedirs(os.path.join(project_path, 'static', 'css'))
        
        # Create CSS file
        with open(os.path.join(project_path, 'static', 'css', 'style.css'), 'w') as f:
            f.write("""body {
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
""")
        
        # Create public directory
        os.makedirs(os.path.join(project_path, 'public', 'docs'))
        
        # Create a documentation file
        with open(os.path.join(project_path, 'public', 'docs', 'guide.html'), 'w') as f:
            f.write("""<!DOCTYPE html>
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
""")
    else:
        # Create a full project based on the selected template
        templates_dir = os.path.join(project_path, 'templates')
        static_dir = os.path.join(project_path, 'static')
        public_dir = os.path.join(project_path, 'public')
        
        # Create basic directories
        os.makedirs(templates_dir)
        os.makedirs(os.path.join(static_dir, 'css'))
        os.makedirs(os.path.join(static_dir, 'js'))
        os.makedirs(os.path.join(static_dir, 'img'))
        os.makedirs(os.path.join(public_dir, 'assets'))
        os.makedirs(os.path.join(public_dir, 'docs'))
        
        # Create CSS file
        with open(os.path.join(static_dir, 'css', 'style.css'), 'w') as f:
            f.write("""/* Main application styles */
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 0;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

header {
    background-color: #333;
    color: white;
    padding: 1rem 0;
}

header .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

nav ul {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
}

nav li {
    margin-left: 20px;
}

nav a {
    color: white;
    text-decoration: none;
}

nav a:hover {
    text-decoration: underline;
}

main {
    padding: 2rem 0;
}

footer {
    background-color: #f5f5f5;
    padding: 1rem 0;
    text-align: center;
    margin-top: 2rem;
}
""")
        
        # Create JavaScript file
        with open(os.path.join(static_dir, 'js', 'app.js'), 'w') as f:
            f.write("""// Main application JavaScript
document.addEventListener('DOMContentLoaded', () => {
    console.log('PyPro application loaded');
});
""")
        
        # Create base template
        with open(os.path.join(templates_dir, 'base.html'), 'w') as f:
            f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ title | default('PyPro App') }}{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css">
    <link rel="stylesheet" href="/static/css/style.css">
    {% block head %}{% endblock %}
</head>
<body data-bs-theme="dark">
    <header>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/">{{ project_name }}</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav ms-auto">
                        <li class="nav-item">
                            <a class="nav-link" href="/">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/about">About</a>
                        </li>
                        {% block nav_items %}{% endblock %}
                    </ul>
                </div>
            </div>
        </nav>
    </header>

    <main>
        <div class="container mt-4">
            {% block content %}{% endblock %}
        </div>
    </main>

    <footer class="bg-dark text-light py-4 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h5>{{ project_name }}</h5>
                    <p>Powered by PyPro Framework</p>
                </div>
                <div class="col-md-6 text-md-end">
                    <p>&copy; {% raw %}{{ now.year }}{% endraw %} {{ project_name }}</p>
                </div>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/static/js/app.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
""")

        if args.template == 'basic' or args.template == 'mvc':
            # Create app structure
            app_dir = os.path.join(project_path, 'app')
            os.makedirs(app_dir)
            
            # Create app/__init__.py
            with open(os.path.join(app_dir, '__init__.py'), 'w') as f:
                f.write(f"""from pypro import PyProApp, Database, SessionMiddleware, CSRFMiddleware, LoggingMiddleware

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
app.use_middleware(LoggingMiddleware)
app.use_middleware(SessionMiddleware, app)
app.use_middleware(CSRFMiddleware, app)

# Import routes
from . import routes

# Set global template variables
@app.context_processor
def inject_globals():
    import datetime
    return {{
        'now': datetime.datetime.now(),
        'project_name': '{project_name}'
    }}
""")
            
            # Create app/routes.py
            with open(os.path.join(app_dir, 'routes.py'), 'w') as f:
                f.write("""from . import app
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

@app.error_handler(404)
def not_found(request, error):
    return render_template('errors/404.html', title='Not Found'), 404

@app.error_handler(500)
def server_error(request, error):
    return render_template('errors/500.html', title='Server Error'), 500
""")
            
            # Create app/models.py
            with open(os.path.join(app_dir, 'models.py'), 'w') as f:
                f.write("""from pypro import Model, Column, Integer, String, DateTime, relationship, ForeignKey
import datetime

class User(Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    posts = relationship('Post', back_populates='author')
    
    def __repr__(self):
        return f'<User {self.username}>'
        
class Post(Model):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    author = relationship('User', back_populates='posts')
    
    def __repr__(self):
        return f'<Post {self.title}>'
""")
            
            # Create app/utils.py
            with open(os.path.join(app_dir, 'utils.py'), 'w') as f:
                f.write("""import datetime

def format_date(dt, format='%B %d, %Y'):
    """Format a date for display.
    
    Args:
        dt: Date or datetime object
        format: Format string
        
    Returns:
        Formatted date string
    """
    return dt.strftime(format)
    
def slugify(text):
    """Convert text to slug format.
    
    Args:
        text: String to convert
        
    Returns:
        Slug-formatted string
    """
    import re
    from unidecode import unidecode
    
    text = unidecode(text).lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'[-]+', '-', text)
    return text.strip('-')
""")
            
            if args.template == 'mvc':
                # Create controllers directory for MVC pattern
                controllers_dir = os.path.join(app_dir, 'controllers')
                os.makedirs(controllers_dir)
                
                # Create app/controllers/__init__.py
                with open(os.path.join(controllers_dir, '__init__.py'), 'w') as f:
                    f.write("""# Import all controllers here
from .home_controller import HomeController
from .user_controller import UserController
""")
                
                # Create app/controllers/base_controller.py
                with open(os.path.join(controllers_dir, 'base_controller.py'), 'w') as f:
                    f.write("""from pypro import PyProApp, render_template

class BaseController:
    """Base controller class for all controllers."""
    
    def __init__(self, app: PyProApp):
        self.app = app
    
    def render(self, template_name, **context):
        """Render a template with the given context.
        
        Args:
            template_name: Name of the template to render
            **context: Context variables to pass to the template
            
        Returns:
            Rendered template response
        """
        return render_template(template_name, **context)
""")
                
                # Create app/controllers/home_controller.py
                with open(os.path.join(controllers_dir, 'home_controller.py'), 'w') as f:
                    f.write("""from .base_controller import BaseController

class HomeController(BaseController):
    """Controller for home and general pages."""
    
    def index(self, request):
        """Handle the home page."""
        return self.render('index.html', title='Welcome to PyPro')
    
    def about(self, request):
        """Handle the about page."""
        return self.render('about.html', title='About')
""")
                
                # Create app/controllers/user_controller.py
                with open(os.path.join(controllers_dir, 'user_controller.py'), 'w') as f:
                    f.write("""from .base_controller import BaseController
from ..models import User

class UserController(BaseController):
    """Controller for user-related pages."""
    
    def profile(self, request, username):
        """Handle user profile page."""
        # In a real app, you would fetch the user from the database
        user = {'username': username, 'bio': 'Example user bio'}
        return self.render('users/profile.html', title=f'Profile: {username}', user=user)
    
    def list(self, request):
        """Handle user listing page."""
        # In a real app, you would fetch users from the database
        users = [
            {'username': 'user1', 'email': 'user1@example.com'},
            {'username': 'user2', 'email': 'user2@example.com'}
        ]
        return self.render('users/list.html', title='Users', users=users)
""")
                
                # Update app/routes.py for MVC pattern
                with open(os.path.join(app_dir, 'routes.py'), 'w') as f:
                    f.write("""from . import app
from pypro import render_template
from .controllers import HomeController, UserController

# Initialize controllers
home_controller = HomeController(app)
user_controller = UserController(app)

# Register routes
app.route('/')(home_controller.index)
app.route('/about')(home_controller.about)
app.route('/users')(user_controller.list)
app.route('/users/<username>')(user_controller.profile)

@app.route('/api/hello/<name>')
def api_hello(request, name):
    return {'message': f'Hello, {name}!'}

@app.error_handler(404)
def not_found(request, error):
    return render_template('errors/404.html', title='Not Found'), 404

@app.error_handler(500)
def server_error(request, error):
    return render_template('errors/500.html', title='Server Error'), 500
""")
                
                # Create users template directory
                os.makedirs(os.path.join(templates_dir, 'users'))
                
                # Create users/profile.html
                with open(os.path.join(templates_dir, 'users', 'profile.html'), 'w') as f:
                    f.write("""{% extends "base.html" %}

{% block content %}
<div class="container mt-4">
    <h1>{{ user.username }}</h1>
    <p>{{ user.bio }}</p>
</div>
{% endblock %}
""")
                
                # Create users/list.html
                with open(os.path.join(templates_dir, 'users', 'list.html'), 'w') as f:
                    f.write("""{% extends "base.html" %}

{% block content %}
<div class="container mt-4">
    <h1>Users</h1>
    <ul class="list-group mt-3">
        {% for user in users %}
        <li class="list-group-item">
            <a href="/users/{{ user.username }}">{{ user.username }}</a>
            <small class="text-muted">{{ user.email }}</small>
        </li>
        {% endfor %}
    </ul>
</div>
{% endblock %}
""")
        
        elif args.template == 'api':
            # Create API-focused project
            api_dir = os.path.join(project_path, 'api')
            os.makedirs(api_dir)
            
            # Create api/__init__.py
            with open(os.path.join(api_dir, '__init__.py'), 'w') as f:
                f.write("""from pypro import PyProApp, CORSMiddleware, RateLimitingMiddleware

app = PyProApp(__name__, template_folder='../templates')

# Configure the app
app.config.update({
    'DEBUG': True,
    'API_VERSION': 'v1',
})

# Add middleware
app.use_middleware(CORSMiddleware, 
                  allow_origins=['*'],
                  allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
                  allow_headers=['Content-Type', 'Authorization'])
app.use_middleware(RateLimitingMiddleware, max_requests=100, time_window=60)

# Import routes
from . import routes
""")
            
            # Create api/routes.py
            with open(os.path.join(api_dir, 'routes.py'), 'w') as f:
                f.write("""from . import app
from pypro import render_template
import json

# API routes
@app.route('/api/users')
def get_users(request):
    """Get a list of users."""
    users = [
        {'id': 1, 'username': 'user1', 'email': 'user1@example.com'},
        {'id': 2, 'username': 'user2', 'email': 'user2@example.com'}
    ]
    return {'users': users}

@app.route('/api/users/<int:user_id>')
def get_user(request, user_id):
    """Get a specific user by ID."""
    # In a real app, you would fetch the user from a database
    user = {'id': user_id, 'username': f'user{user_id}', 'email': f'user{user_id}@example.com'}
    return {'user': user}

@app.route('/api/posts')
def get_posts(request):
    """Get a list of posts."""
    posts = [
        {'id': 1, 'title': 'First Post', 'content': 'Hello world', 'author_id': 1},
        {'id': 2, 'title': 'Second Post', 'content': 'Another post', 'author_id': 2}
    ]
    return {'posts': posts}

@app.route('/api/docs')
def api_docs(request):
    """Render API documentation page."""
    return render_template('api_docs.html', title='API Documentation')

# Web routes for documentation
@app.route('/')
def index(request):
    """Render the home page with API information."""
    return render_template('index.html', title='API Home')
""")
            
            # Create api/schema.py
            with open(os.path.join(api_dir, 'schema.py'), 'w') as f:
                f.write('''"""API schema definitions.

This module contains JSON schema definitions for API requests and responses.
"""

# User schema
user_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "username": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "created_at": {"type": "string", "format": "date-time"}
    },
    "required": ["id", "username", "email"]
}

# Post schema
post_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "content": {"type": "string"},
        "author_id": {"type": "integer"},
        "created_at": {"type": "string", "format": "date-time"}
    },
    "required": ["id", "title", "content", "author_id"]
}

# Error schema
error_schema = {
    "type": "object",
    "properties": {
        "error": {"type": "string"},
        "code": {"type": "integer"},
        "details": {"type": "string"}
    },
    "required": ["error", "code"]
}
""")
            
            # Create api_docs.html template
            with open(os.path.join(templates_dir, 'api_docs.html'), 'w') as f:
                f.write("""{% extends "base.html" %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-3">
            <div class="sticky-top pt-4">
                <div class="list-group">
                    <a href="#introduction" class="list-group-item list-group-item-action">Introduction</a>
                    <a href="#authentication" class="list-group-item list-group-item-action">Authentication</a>
                    <a href="#users" class="list-group-item list-group-item-action">Users API</a>
                    <a href="#posts" class="list-group-item list-group-item-action">Posts API</a>
                    <a href="#errors" class="list-group-item list-group-item-action">Error Handling</a>
                </div>
            </div>
        </div>
        <div class="col-md-9">
            <h1>API Documentation</h1>
            
            <section id="introduction" class="mb-5">
                <h2>Introduction</h2>
                <p>Welcome to the API documentation. This API follows RESTful principles and returns JSON responses.</p>
                <p>Base URL: <code>/api</code></p>
            </section>
            
            <section id="authentication" class="mb-5">
                <h2>Authentication</h2>
                <p>This API uses token-based authentication. Include your API key in the Authorization header:</p>
                <pre><code>Authorization: Bearer YOUR_API_KEY</code></pre>
            </section>
            
            <section id="users" class="mb-5">
                <h2>Users API</h2>
                
                <div class="card mb-4">
                    <div class="card-header bg-primary text-white">
                        <strong>GET</strong> /api/users
                    </div>
                    <div class="card-body">
                        <p>Get a list of all users.</p>
                        <h5>Parameters</h5>
                        <ul>
                            <li><code>limit</code> (optional): Maximum number of users to return</li>
                            <li><code>offset</code> (optional): Number of users to skip</li>
                        </ul>
                        <h5>Response</h5>
                        <pre><code>{
  "users": [
    {
      "id": 1,
      "username": "user1",
      "email": "user1@example.com"
    },
    {
      "id": 2,
      "username": "user2",
      "email": "user2@example.com"
    }
  ]
}</code></pre>
                    </div>
                </div>
                
                <div class="card mb-4">
                    <div class="card-header bg-primary text-white">
                        <strong>GET</strong> /api/users/:id
                    </div>
                    <div class="card-body">
                        <p>Get a specific user by ID.</p>
                        <h5>Parameters</h5>
                        <ul>
                            <li><code>id</code> (required): User ID</li>
                        </ul>
                        <h5>Response</h5>
                        <pre><code>{
  "user": {
    "id": 1,
    "username": "user1",
    "email": "user1@example.com"
  }
}</code></pre>
                    </div>
                </div>
            </section>
            
            <section id="posts" class="mb-5">
                <h2>Posts API</h2>
                
                <div class="card mb-4">
                    <div class="card-header bg-primary text-white">
                        <strong>GET</strong> /api/posts
                    </div>
                    <div class="card-body">
                        <p>Get a list of all posts.</p>
                        <h5>Response</h5>
                        <pre><code>{
  "posts": [
    {
      "id": 1,
      "title": "First Post",
      "content": "Hello world",
      "author_id": 1
    },
    {
      "id": 2,
      "title": "Second Post",
      "content": "Another post",
      "author_id": 2
    }
  ]
}</code></pre>
                    </div>
                </div>
            </section>
            
            <section id="errors" class="mb-5">
                <h2>Error Handling</h2>
                <p>When an error occurs, the API will return an error object with the following format:</p>
                <pre><code>{
  "error": "Error message",
  "code": 400,
  "details": "Additional error details"
}</code></pre>
                
                <h5>Common Error Codes</h5>
                <ul>
                    <li><code>400</code>: Bad Request</li>
                    <li><code>401</code>: Unauthorized</li>
                    <li><code>403</code>: Forbidden</li>
                    <li><code>404</code>: Not Found</li>
                    <li><code>500</code>: Internal Server Error</li>
                </ul>
            </section>
        </div>
    </div>
</div>
{% endblock %}
""")
        
        elif args.template == 'spa':
            # Create a Single Page Application backend
            app_dir = os.path.join(project_path, 'app')
            os.makedirs(app_dir)
            
            # Create app/__init__.py
            with open(os.path.join(app_dir, '__init__.py'), 'w') as f:
                f.write("""from pypro import PyProApp, CORSMiddleware, render_template

app = PyProApp(__name__, 
               template_folder='../templates',
               static_folder='../static',
               public_folder='../public')

# Configure the app
app.config.update({
    'DEBUG': True,
    'SPA_MODE': True,
})

# Add middleware for API
app.use_middleware(CORSMiddleware, 
                  allow_origins=['*'],
                  allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
                  allow_headers=['Content-Type', 'Authorization'])

# Import routes
from . import routes
""")
            
            # Create app/routes.py
            with open(os.path.join(app_dir, 'routes.py'), 'w') as f:
                f.write("""from . import app
from pypro import render_template

# API routes for SPA
@app.route('/api/data')
def get_data(request):
    """Get initial data for the SPA."""
    return {
        'title': 'PyPro SPA',
        'items': [
            {'id': 1, 'name': 'Item 1', 'description': 'First item'},
            {'id': 2, 'name': 'Item 2', 'description': 'Second item'},
            {'id': 3, 'name': 'Item 3', 'description': 'Third item'}
        ]
    }

# SPA route - all non-API routes serve the main SPA
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def spa(request, path=''):
    """Serve the SPA for all non-API routes."""
    # Skip API routes
    if path.startswith('api/') or path.startswith('static/') or path.startswith('public/'):
        return None  # Let the next route handler take over
        
    return render_template('index.html')
""")
            
            # Create SPA index.html
            with open(os.path.join(templates_dir, 'index.html'), 'w') as f:
                f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PyPro SPA</title>
    <link rel="stylesheet" href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css">
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body data-bs-theme="dark">
    <div id="app">
        <!-- App content will be loaded here -->
        <div class="container mt-5">
            <h1>Loading...</h1>
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    </div>
    
    <!-- App templates -->
    <template id="home-template">
        <div class="container mt-4">
            <h1>{{title}}</h1>
            <p>Welcome to the PyPro Single Page Application</p>
            
            <div class="row mt-4">
                <div class="col-md-4">
                    <div class="list-group">
                        <a href="#/" class="list-group-item list-group-item-action active">Home</a>
                        <a href="#/items" class="list-group-item list-group-item-action">Items</a>
                        <a href="#/about" class="list-group-item list-group-item-action">About</a>
                    </div>
                </div>
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">PyPro SPA Starter</h5>
                            <p class="card-text">
                                This is a Single Page Application starter template for PyPro.
                                It uses vanilla JavaScript for simplicity, but you can easily
                                integrate with frameworks like Vue.js or React.
                            </p>
                            <button class="btn btn-primary" id="load-data-btn">Load Data</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </template>
    
    <template id="items-template">
        <div class="container mt-4">
            <h1>Items</h1>
            
            <div class="row mt-4">
                <div class="col-md-4">
                    <div class="list-group">
                        <a href="#/" class="list-group-item list-group-item-action">Home</a>
                        <a href="#/items" class="list-group-item list-group-item-action active">Items</a>
                        <a href="#/about" class="list-group-item list-group-item-action">About</a>
                    </div>
                </div>
                <div class="col-md-8">
                    <div class="list-group" id="items-list">
                        <!-- Items will be loaded here -->
                    </div>
                </div>
            </div>
        </div>
    </template>
    
    <template id="about-template">
        <div class="container mt-4">
            <h1>About</h1>
            
            <div class="row mt-4">
                <div class="col-md-4">
                    <div class="list-group">
                        <a href="#/" class="list-group-item list-group-item-action">Home</a>
                        <a href="#/items" class="list-group-item list-group-item-action">Items</a>
                        <a href="#/about" class="list-group-item list-group-item-action active">About</a>
                    </div>
                </div>
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">About This App</h5>
                            <p class="card-text">
                                This is a simple SPA built with the PyPro framework.
                                The backend serves a single HTML page and API endpoints,
                                while the frontend handles routing and rendering.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </template>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/static/js/app.js"></script>
    <script src="/static/js/router.js"></script>
</body>
</html>
""")
            
            # Create router.js
            with open(os.path.join(static_dir, 'js', 'router.js'), 'w') as f:
                f.write("""// Simple SPA router
class Router {
    constructor(routes) {
        this.routes = routes;
        this.currentRoute = null;
        
        // Handle route changes
        window.addEventListener('hashchange', () => this.handleRouteChange());
        
        // Initial route
        this.handleRouteChange();
    }
    
    handleRouteChange() {
        const hash = window.location.hash || '#/';
        const path = hash.substring(1);
        
        // Find matching route
        const route = this.routes.find(r => path.match(r.path));
        
        if (route) {
            this.currentRoute = route;
            this.loadRoute(route, path);
        } else {
            // Default to home or 404
            const defaultRoute = this.routes.find(r => r.path === '/' || r.path === '*');
            if (defaultRoute) {
                this.currentRoute = defaultRoute;
                this.loadRoute(defaultRoute, path);
            }
        }
    }
    
    loadRoute(route, path) {
        const appElement = document.getElementById('app');
        const template = document.getElementById(`${route.name}-template`);
        
        if (template) {
            appElement.innerHTML = template.innerHTML;
            
            // Call controller if it exists
            if (route.controller) {
                route.controller(path);
            }
        } else {
            appElement.innerHTML = '<div class="container mt-5"><h1>Error: Template not found</h1></div>';
        }
    }
    
    navigate(path) {
        window.location.hash = `#${path}`;
    }
}

// Initialize after DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // App data
    window.appData = {
        title: 'PyPro SPA',
        items: []
    };
    
    // Define routes
    const routes = [
        {
            path: '/',
            name: 'home',
            controller: () => {
                const button = document.getElementById('load-data-btn');
                if (button) {
                    button.addEventListener('click', async () => {
                        try {
                            const response = await fetch('/api/data');
                            const data = await response.json();
                            alert(`Loaded ${data.items.length} items!`);
                            window.appData.items = data.items;
                        } catch (error) {
                            console.error('Error loading data:', error);
                        }
                    });
                }
                
                // Replace template variables
                document.querySelector('h1').textContent = window.appData.title;
            }
        },
        {
            path: '/items',
            name: 'items',
            controller: async () => {
                // Load data if not already loaded
                if (window.appData.items.length === 0) {
                    try {
                        const response = await fetch('/api/data');
                        const data = await response.json();
                        window.appData.items = data.items;
                    } catch (error) {
                        console.error('Error loading data:', error);
                    }
                }
                
                // Render items
                const itemsList = document.getElementById('items-list');
                if (itemsList) {
                    itemsList.innerHTML = '';
                    window.appData.items.forEach(item => {
                        const element = document.createElement('a');
                        element.href = `#/items/${item.id}`;
                        element.className = 'list-group-item list-group-item-action';
                        element.innerHTML = `
                            <h5>${item.name}</h5>
                            <p>${item.description}</p>
                        `;
                        itemsList.appendChild(element);
                    });
                }
            }
        },
        {
            path: '/about',
            name: 'about',
            controller: () => {
                // Nothing special needed for about page
            }
        },
        {
            path: '*',
            name: 'home',  // Default to home template
            controller: () => {
                console.log('404 - Route not found');
            }
        }
    ];
    
    // Initialize router
    window.router = new Router(routes);
});
""")
            
            # Update app.js for SPA
            with open(os.path.join(static_dir, 'js', 'app.js'), 'w') as f:
                f.write("""// Main application JavaScript
document.addEventListener('DOMContentLoaded', () => {
    console.log('PyPro SPA loaded');
});

// Helper functions
function htmlToElement(html) {
    const template = document.createElement('template');
    template.innerHTML = html.trim();
    return template.content.firstChild;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString();
}
""")
        
        # Create common templates for all project types
        # Create index.html if not SPA template
        if args.template != 'spa':
            with open(os.path.join(templates_dir, 'index.html'), 'w') as f:
                f.write("""{% extends "base.html" %}

{% block content %}
<div class="row mt-4">
    <div class="col-md-12">
        <div class="jumbotron bg-light p-5 rounded">
            <h1 class="display-4">Welcome to {{ project_name }}</h1>
            <p class="lead">A PyPro application</p>
            <hr class="my-4">
            <p>PyPro is a Python web framework with "batteries included" design philosophy.</p>
            <a class="btn btn-primary" href="/about" role="button">Learn more</a>
        </div>
    </div>
</div>

<div class="row mt-4">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">Getting Started</h5>
            </div>
            <div class="card-body">
                <p class="card-text">
                    PyPro makes it easy to build web applications quickly.
                    Here are some useful links to get started:
                </p>
                <ul>
                    <li><a href="/public/docs/guide.html">Documentation</a></li>
                    <li><a href="https://github.com/user/pypro">GitHub Repository</a></li>
                </ul>
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">Features</h5>
            </div>
            <div class="card-body">
                <ul>
                    <li>Simple and intuitive API</li>
                    <li>Built-in template rendering</li>
                    <li>Database integration</li>
                    <li>Middleware support</li>
                    <li>Error handling</li>
                    <li>Static and public file serving</li>
                </ul>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")
            
            # Create about.html if not SPA template
            with open(os.path.join(templates_dir, 'about.html'), 'w') as f:
                f.write("""{% extends "base.html" %}

{% block content %}
<div class="row mt-4">
    <div class="col-md-12">
        <h1>About {{ project_name }}</h1>
        <p class="lead">Learn more about this PyPro application.</p>
    </div>
</div>

<div class="row mt-4">
    <div class="col-md-8">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">About PyPro</h5>
                <p class="card-text">
                    PyPro is a Python web framework with "batteries included" design philosophy.
                    It provides everything you need to build modern web applications:
                </p>
                <ul>
                    <li><strong>Routing and URL dispatch</strong>: Easy to define routes with path parameters</li>
                    <li><strong>Template rendering</strong>: Built-in Jinja2 integration</li>
                    <li><strong>Database ORM</strong>: Simple database models with SQLAlchemy support</li>
                    <li><strong>Security features</strong>: CSRF protection, secure cookies, etc.</li>
                    <li><strong>Session management</strong>: Server-side sessions or cookie-based sessions</li>
                    <li><strong>Middleware</strong>: Extensible middleware system</li>
                    <li><strong>Static file handling</strong>: Serve static files efficiently</li>
                    <li><strong>Public folder</strong>: Serve files directly from the root path</li>
                </ul>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">Project Info</h5>
            </div>
            <div class="card-body">
                <p><strong>Project name:</strong> {{ project_name }}</p>
                <p><strong>Framework:</strong> PyPro</p>
                <p><strong>Created at:</strong> {% raw %}{{ now.strftime('%Y-%m-%d') }}{% endraw %}</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")
        
        # Create error templates for all project types
        os.makedirs(os.path.join(templates_dir, 'errors'))
        
        # Create 404 template
        with open(os.path.join(templates_dir, 'errors', '404.html'), 'w') as f:
            f.write("""{% extends "base.html" %}

{% block content %}
<div class="container mt-5">
    <div class="row">
        <div class="col-md-6 offset-md-3 text-center">
            <h1 class="display-1">404</h1>
            <h2>Page Not Found</h2>
            <p class="lead">The page you are looking for doesn't exist or has been moved.</p>
            <a href="/" class="btn btn-primary">Go Home</a>
        </div>
    </div>
</div>
{% endblock %}
""")
        
        # Create 500 template
        with open(os.path.join(templates_dir, 'errors', '500.html'), 'w') as f:
            f.write("""{% extends "base.html" %}

{% block content %}
<div class="container mt-5">
    <div class="row">
        <div class="col-md-6 offset-md-3 text-center">
            <h1 class="display-1">500</h1>
            <h2>Server Error</h2>
            <p class="lead">Something went wrong on our end. Please try again later.</p>
            <a href="/" class="btn btn-primary">Go Home</a>
        </div>
    </div>
</div>
{% endblock %}
""")
        
        # Create main.py entry point
        with open(os.path.join(project_path, 'main.py'), 'w') as f:
            if args.template == 'api':
                f.write("""from api import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
""")
            elif args.template == 'spa':
                f.write("""from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
""")
            else:
                f.write("""from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
""")
        
        # Create README.md
        with open(os.path.join(project_path, 'README.md'), 'w') as f:
            f.write(f"""# {project_name}

A PyPro web application using the {args.template} template.

## Setup

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Run the application:

```
python main.py
```

Or with the PyPro CLI:

```
pyp run main.py
```

## Project Structure

- {'`api/`' if args.template == 'api' else '`app/`'} - Application package
  - `__init__.py` - Application factory
  {f'- `controllers/` - MVC controllers' if args.template == 'mvc' else ''}
  - `routes.py` - Route definitions
  {'- `models.py` - Data models' if args.template != 'api' else ''}
  {'- `utils.py` - Utility functions' if args.template != 'api' else ''}
  {'- `schema.py` - API schema definitions' if args.template == 'api' else ''}
- `static/` - Static files (CSS, JavaScript, etc.)
  - `css/` - CSS stylesheets
  - `js/` - JavaScript files
  - `img/` - Images
- `public/` - Publicly accessible files (served from root path)
  - `assets/` - Public assets
  - `docs/` - Documentation
- `templates/` - HTML templates
- `main.py` - Application entry point

## Features

- {
    'RESTful API with CORS and rate limiting' if args.template == 'api' else 
    'Single Page Application (SPA) with client-side routing' if args.template == 'spa' else
    'MVC architecture with controllers' if args.template == 'mvc' else
    'Basic web application with templates'
  }
- Bootstrap styling
- Public folder for direct file access
- Error handling
- {'API documentation page' if args.template == 'api' else 'Responsive design'}
""")
        
        # Create requirements.txt
        with open(os.path.join(project_path, 'requirements.txt'), 'w') as f:
            f.write(f"""pypro
gunicorn
{'unidecode' if args.template == 'mvc' else ''}
""")
        
        # Create public/docs/guide.html
        os.makedirs(os.path.join(public_dir, 'docs'), exist_ok=True)
        with open(os.path.join(public_dir, 'docs', 'guide.html'), 'w') as f:
            f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>{project_name} - Documentation</title>
    <link rel="stylesheet" href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        pre {{
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        code {{
            background-color: #f5f5f5;
            padding: 2px 4px;
            border-radius: 3px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .navbar {{
            margin-bottom: 20px;
        }}
    </style>
</head>
<body data-bs-theme="dark">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">{project_name}</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link active" href="/public/docs/guide.html">Documentation</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="row">
            <div class="col-md-3">
                <div class="sticky-top pt-3">
                    <div class="list-group">
                        <a href="#getting-started" class="list-group-item list-group-item-action">Getting Started</a>
                        <a href="#project-structure" class="list-group-item list-group-item-action">Project Structure</a>
                        <a href="#routes" class="list-group-item list-group-item-action">Routes</a>
                        <a href="#templates" class="list-group-item list-group-item-action">Templates</a>
                        <a href="#static-files" class="list-group-item list-group-item-action">Static Files</a>
                        <a href="#public-folder" class="list-group-item list-group-item-action">Public Folder</a>
                        {'<a href="#api" class="list-group-item list-group-item-action">API</a>' if args.template == 'api' else ''}
                        {'<a href="#spa" class="list-group-item list-group-item-action">SPA Architecture</a>' if args.template == 'spa' else ''}
                        {'<a href="#mvc" class="list-group-item list-group-item-action">MVC Pattern</a>' if args.template == 'mvc' else ''}
                    </div>
                </div>
            </div>
            <div class="col-md-9">
                <h1>{project_name} Documentation</h1>
                <p>Welcome to the documentation for your PyPro project.</p>
                
                <section id="getting-started" class="mb-5">
                    <h2>Getting Started</h2>
                    <p>To run your PyPro application:</p>
                    <pre><code>$ python main.py</code></pre>
                    <p>Or with the PyPro CLI:</p>
                    <pre><code>$ pyp run main.py</code></pre>
                    <p>The application will be available at <code>http://localhost:5000</code>.</p>
                </section>
                
                <section id="project-structure" class="mb-5">
                    <h2>Project Structure</h2>
                    <pre><code>
{project_name}/
  ├── {'api/' if args.template == 'api' else 'app/'}         # Application package
  │   ├── __init__.py   # Application factory
  │   ├── routes.py     # Route definitions
{f'  │   ├── models.py    # Data models' if args.template != 'api' else ''}
{f'  │   ├── utils.py     # Utility functions' if args.template != 'api' else ''}
{f'  │   └── schema.py    # API schema definitions' if args.template == 'api' else ''}
{f'  │   └── controllers/ # MVC controllers' if args.template == 'mvc' else ''}
  ├── static/          # Static files
  │   ├── css/         # CSS stylesheets
  │   ├── js/          # JavaScript files
  │   └── img/         # Images
  ├── public/          # Public files (served from root)
  │   ├── assets/      # Public assets
  │   └── docs/        # Documentation
  ├── templates/       # HTML templates
  ├── main.py          # Application entry point
  └── README.md        # Project README
                    </code></pre>
                </section>
                
                <section id="routes" class="mb-5">
                    <h2>Routes</h2>
                    <p>Routes are defined in the <code>{'api' if args.template == 'api' else 'app'}/routes.py</code> file:</p>
                    <pre><code>
@app.route('/')
def index(request):
    return render_template('index.html', title='Welcome')

@app.route('/about')
def about(request):
    return render_template('about.html', title='About')

@app.route('/api/hello/<name>')
def api_hello(request, name):
    return {{'message': f'Hello, {{name}}!'}}
                    </code></pre>
                </section>
                
                <section id="templates" class="mb-5">
                    <h2>Templates</h2>
                    <p>Templates are stored in the <code>templates/</code> directory and use Jinja2 syntax:</p>
                    <pre><code>
&lt;!-- templates/base.html --&gt;
&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;{% block title %}{{ title }}{% endblock %}&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    {% block content %}{% endblock %}
&lt;/body&gt;
&lt;/html&gt;

&lt;!-- templates/index.html --&gt;
{% extends "base.html" %}

{% block content %}
    &lt;h1&gt;{{ title }}&lt;/h1&gt;
    &lt;p&gt;Welcome to your PyPro application!&lt;/p&gt;
{% endblock %}
                    </code></pre>
                </section>
                
                <section id="static-files" class="mb-5">
                    <h2>Static Files</h2>
                    <p>Static files are stored in the <code>static/</code> directory and are served from the <code>/static/</code> URL path:</p>
                    <pre><code>&lt;link rel="stylesheet" href="/static/css/style.css"&gt;</code></pre>
                </section>
                
                <section id="public-folder" class="mb-5">
                    <h2>Public Folder</h2>
                    <p>The <code>public/</code> folder contains files that are served directly from the root URL path:</p>
                    <pre><code>&lt;a href="/docs/guide.html"&gt;Documentation&lt;/a&gt;</code></pre>
                    <p>This is useful for files like <code>robots.txt</code>, <code>favicon.ico</code>, and other files that need to be accessible from the root path.</p>
                </section>
                
                {"""<section id="api" class="mb-5">
                    <h2>API</h2>
                    <p>This project is set up as an API with the following features:</p>
                    <ul>
                        <li>CORS support for cross-origin requests</li>
                        <li>Rate limiting to prevent abuse</li>
                        <li>JSON schema validation</li>
                    </ul>
                    <p>API endpoints are defined in <code>api/routes.py</code> and return JSON responses:</p>
                    <pre><code>
@app.route('/api/users')
def get_users(request):
    \"\"\"Get a list of users.\"\"\"
    users = [
        {'id': 1, 'username': 'user1', 'email': 'user1@example.com'},
        {'id': 2, 'username': 'user2', 'email': 'user2@example.com'}
    ]
    return {'users': users}
                    </code></pre>
                </section>""" if args.template == 'api' else ''}
                
                {"""<section id="spa" class="mb-5">
                    <h2>SPA Architecture</h2>
                    <p>This project is set up as a Single Page Application (SPA) with the following features:</p>
                    <ul>
                        <li>Client-side routing with hash-based navigation</li>
                        <li>Template-based rendering</li>
                        <li>API integration</li>
                    </ul>
                    <p>The SPA is implemented in <code>static/js/router.js</code> and <code>static/js/app.js</code>.</p>
                    <p>The backend serves a single HTML page and API endpoints, while the frontend handles routing and rendering:</p>
                    <pre><code>
// Simplified router implementation
class Router {
    constructor(routes) {
        this.routes = routes;
        window.addEventListener('hashchange', 
                               () => this.handleRouteChange());
        this.handleRouteChange();
    }
    
    handleRouteChange() {
        const hash = window.location.hash || '#/';
        const path = hash.substring(1);
        const route = this.routes.find(r => path.match(r.path));
        
        if (route) {
            this.loadRoute(route, path);
        }
    }
    // ...
}
                    </code></pre>
                </section>""" if args.template == 'spa' else ''}
                
                {"""<section id="mvc" class="mb-5">
                    <h2>MVC Pattern</h2>
                    <p>This project follows the Model-View-Controller (MVC) pattern:</p>
                    <ul>
                        <li><strong>Models</strong>: Defined in <code>app/models.py</code></li>
                        <li><strong>Views</strong>: Templates in <code>templates/</code></li>
                        <li><strong>Controllers</strong>: Located in <code>app/controllers/</code></li>
                    </ul>
                    <p>Controllers handle request processing and returning responses:</p>
                    <pre><code>
class HomeController(BaseController):
    \"\"\"Controller for home and general pages.\"\"\"
    
    def index(self, request):
        \"\"\"Handle the home page.\"\"\"
        return self.render('index.html', title='Welcome to PyPro')
    
    def about(self, request):
        \"\"\"Handle the about page.\"\"\"
        return self.render('about.html', title='About')
                    </code></pre>
                    <p>Routes are registered in <code>app/routes.py</code>:</p>
                    <pre><code>
# Initialize controllers
home_controller = HomeController(app)
user_controller = UserController(app)

# Register routes
app.route('/')(home_controller.index)
app.route('/about')(home_controller.about)
app.route('/users')(user_controller.list)
app.route('/users/<username>')(user_controller.profile)
                    </code></pre>
                </section>""" if args.template == 'mvc' else ''}
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
""")
    
    # Print success message with project details
    print(f"\n✅ Successfully created a new PyPro project in {project_path}")
    if args.minimal:
        print("\nThis is a minimal project with a simple structure:")
        print("- app.py - Main application file")
        print("- templates/ - HTML templates")
        print("- static/ - Static files")
        print("- public/ - Public files")
    else:
        print(f"\nThis is a {args.template} project with the following structure:")
        if args.template == 'api':
            print("- api/ - API application package")
        else:
            print("- app/ - Application package")
        if args.template == 'mvc':
            print("  - controllers/ - MVC controllers")
        print("- static/ - Static files")
        print("- public/ - Public files")
        print("- templates/ - HTML templates")
    
    print("\nTo run the application:")
    print(f"cd {project_path}")
    print("python main.py")
    
    print("\nOr with the PyPro CLI:")
    print(f"cd {project_path} && pyp run main.py")
    
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
    with open(os.path.join(app_dir, '__init__.py'), 'w') as f:
        f.write(f""""""Module {app_name} for the PyPro application."""

from pypro import PyProApp

# Create a sub-app
app = PyProApp(__name__)

# Import routes
from . import routes
""")
    
    # Create routes.py
    with open(os.path.join(app_dir, 'routes.py'), 'w') as f:
        f.write(f""""""Routes for the {app_name} module."""

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
""")
    
    # Create models.py
    with open(os.path.join(app_dir, 'models.py'), 'w') as f:
        f.write(f""""""Models for the {app_name} module."""

from pypro import Model, Column, Integer, String, DateTime
import datetime

class {app_name.title()}(Model):
    """Model for {app_name}."""
    
    __tablename__ = '{app_name.lower()}'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f'<{app_name.title()} {{self.name}}>'
""")
    
    # Create utils.py
    with open(os.path.join(app_dir, 'utils.py'), 'w') as f:
        f.write(f""""""Utilities for the {app_name} module."""

def format_name(name):
    """Format a name for display."""
    return name.title()
""")
    
    # Create templates directory
    templates_dir = os.path.join(project_dir, 'templates', app_name)
    os.makedirs(templates_dir, exist_ok=True)
    
    # Create index.html
    with open(os.path.join(templates_dir, 'index.html'), 'w') as f:
        f.write(f"""{% extends "base.html" %}

{% block content %}
<div class="container mt-4">
    <h1>{{ title }}</h1>
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
{% endblock %}
""")
    
    # Create details.html
    with open(os.path.join(templates_dir, 'details.html'), 'w') as f:
        f.write(f"""{% extends "base.html" %}

{% block content %}
<div class="container mt-4">
    <h1>{{ title }}</h1>
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
                <li><code>models.py</code>: Data models</li>
                <li><code>utils.py</code>: Utility functions</li>
            </ul>
        </div>
    </div>
    
    <a href="/{app_name}" class="btn btn-primary mt-3">Back to {app_name.title()}</a>
</div>
{% endblock %}
""")
    
    # Update the main app's routes to include the new app
    main_app_file = os.path.join(project_dir, 'app', '__init__.py')
    if os.path.exists(main_app_file):
        try:
            with open(main_app_file, 'r') as f:
                content = f.read()
                
            # Check if the module is already imported
            import_string = f"from .. import {app_name}"
            mount_string = f"app.mount('/{app_name}', {app_name}.app)"
            
            new_content = content
            
            # Add import if needed
            if import_string not in content:
                if "# Import routes" in content:
                    new_content = new_content.replace("# Import routes", f"# Import routes\n{import_string}")
                else:
                    # Append at the end
                    new_content += f"\n\n# Import sub-applications\n{import_string}\n"
            
            # Add mount if needed
            if mount_string not in new_content:
                new_content += f"\n\n# Mount sub-applications\n{mount_string}\n"
                
            # Update file if changed
            if new_content != content:
                with open(main_app_file, 'w') as f:
                    f.write(new_content)
                    
                print(f"✅ Updated {main_app_file} to include the {app_name} module")
            
        except Exception as e:
            print(f"⚠️ Could not update main app file: {e}")
            print(f"You'll need to manually import and mount the {app_name} module in your main app.")
    
    print(f"\n✅ Successfully created a new app module '{app_name}' in {app_dir}")
    print("\nDirectory structure:")
    print(f"- {app_name}/")
    print(f"  - __init__.py")
    print(f"  - routes.py")
    print(f"  - models.py")
    print(f"  - utils.py")
    print(f"- templates/{app_name}/")
    print(f"  - index.html")
    print(f"  - details.html")
    
    print(f"\nTo use this module, import and mount it in your main application:")
    print(f"from {app_name} import app as {app_name}_app")
    print(f"app.mount('/{app_name}', {app_name}_app)")
    
    return 0


def db_command(args: argparse.Namespace):
    """
    Handle database commands.
    
    Args:
        args: Command-line arguments
    """
    if not args.db_command:
        logging.error("No database command specified")
        return 1
        
    app = load_app_from_file(args.file)
    if not app:
        return 1
        
    # Import needed modules
    try:
        from .db import Database, Migration
    except ImportError as e:
        logging.error(f"Error importing database modules: {e}")
        return 1
        
    # Initialize database connection
    db = Database(app)
    
    if args.db_command == 'init':
        # Initialize database
        print("Initializing database...")
        # This will create tables for all models
        return 0
        
    elif args.db_command == 'migrate':
        # Create a new migration
        migration = Migration(db)
        migration.generate(args.name)
        return 0
        
    elif args.db_command == 'upgrade':
        # Apply migrations
        migration = Migration(db)
        print("Applying migrations...")
        migration.migrate(args.target)
        return 0
        
    elif args.db_command == 'downgrade':
        # Roll back migrations
        migration = Migration(db)
        print(f"Rolling back {args.steps} migration(s)...")
        migration.rollback(args.steps)
        return 0
        
    else:
        logging.error(f"Unknown database command: {args.db_command}")
        return 1


def shell_command(args: argparse.Namespace):
    """
    Run a Python shell with PyPro environment.
    
    Args:
        args: Command-line arguments
    """
    # Set up environment
    import code
    import readline
    import rlcompleter
    
    # Set up auto-completion
    readline.parse_and_bind("tab: complete")
    
    # Create locals dictionary
    locals_dict = {
        'pypro': sys.modules['pypro'],
    }
    
    # Add app to locals if file specified
    if args.file:
        app = load_app_from_file(args.file)
        if app:
            locals_dict['app'] = app
    
    # Create banner
    banner = "PyPro Interactive Shell\n"
    if 'app' in locals_dict:
        banner += "App loaded successfully. The 'app' variable is available.\n"
    banner += "Type 'help(pypro)' for help on PyPro."
    
    # Start interactive shell
    code.interact(banner=banner, local=locals_dict)
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
    elif parsed_args.command == 'db':
        return db_command(parsed_args)
    elif parsed_args.command == 'shell':
        return shell_command(parsed_args)
    elif parsed_args.command == 'routes':
        return routes_command(parsed_args)
    else:
        logging.error(f"Unknown command: {parsed_args.command}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
