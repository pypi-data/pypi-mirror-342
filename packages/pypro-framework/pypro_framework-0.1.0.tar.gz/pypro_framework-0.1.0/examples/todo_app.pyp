from pypro import PyProApp, render_template, Model, Column, Integer, String, Boolean, DateTime
import datetime

# Create the application
app = PyProApp(__name__)
app.config['DEBUG'] = True

# Define models
class Task(Model):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Initialize database
from pypro import Database
db = Database(app)

# Define routes
@app.route('/')
def index(request):
    # Get all tasks
    if hasattr(app, 'db'):
        # Use SQLAlchemy
        session = db.get_session()
        tasks = session.query(Task).all()
        session.close()
    else:
        # Use simple database
        tasks = Task.all(db.get_connection())
    
    return render_template('index.html', tasks=tasks)

@app.route('/tasks/new', methods=['GET', 'POST'])
def new_task(request):
    if request.method == 'POST':
        title = request.get_data('title')
        description = request.get_data('description')
        
        if title:
            task = Task(title=title, description=description)
            
            if hasattr(app, 'db'):
                # Use SQLAlchemy
                session = db.get_session()
                session.add(task)
                session.commit()
                session.close()
            else:
                # Use simple database
                task.save(db.get_connection())
            
            return app.response_class.redirect('/')
        
    return render_template('new_task.html')

@app.route('/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(request, task_id):
    if hasattr(app, 'db'):
        # Use SQLAlchemy
        session = db.get_session()
        task = session.query(Task).get(task_id)
        if task:
            task.completed = True
            session.commit()
        session.close()
    else:
        # Use simple database
        task = Task.get(db.get_connection(), task_id)
        if task:
            task.completed = True
            task.save(db.get_connection())
    
    return app.response_class.redirect('/')

@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(request, task_id):
    if hasattr(app, 'db'):
        # Use SQLAlchemy
        session = db.get_session()
        task = session.query(Task).get(task_id)
        if task:
            session.delete(task)
            session.commit()
        session.close()
    else:
        # Use simple database
        task = Task.get(db.get_connection(), task_id)
        if task:
            task.delete(db.get_connection())
    
    return app.response_class.redirect('/')

# Template definitions
templates = {
    'index.html': '''
<!DOCTYPE html>
<html>
<head>
    <title>PyPro Todo App</title>
    <link rel="stylesheet" href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css">
    <style>
        body { padding: 20px; }
        .completed { text-decoration: line-through; }
    </style>
</head>
<body data-bs-theme="dark">
    <div class="container">
        <h1 class="mb-4">Todo List</h1>
        
        <a href="/tasks/new" class="btn btn-primary mb-3">Add New Task</a>
        
        <div class="list-group">
            {% for task in tasks %}
            <div class="list-group-item {% if task.completed %}bg-success bg-opacity-25{% endif %}">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h5 class="mb-1 {% if task.completed %}completed{% endif %}">{{ task.title }}</h5>
                        <p class="mb-1 {% if task.completed %}completed{% endif %}">{{ task.description }}</p>
                        <small>Created: {{ task.created_at.strftime('%Y-%m-%d %H:%M') }}</small>
                    </div>
                    <div class="btn-group" role="group">
                        {% if not task.completed %}
                        <form action="/tasks/{{ task.id }}/complete" method="post">
                            <button type="submit" class="btn btn-success btn-sm">Complete</button>
                        </form>
                        {% endif %}
                        <form action="/tasks/{{ task.id }}/delete" method="post" class="ms-2">
                            <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                        </form>
                    </div>
                </div>
            </div>
            {% else %}
            <div class="list-group-item">
                <p class="mb-0">No tasks yet. Add a new task to get started!</p>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
    ''',
    
    'new_task.html': '''
<!DOCTYPE html>
<html>
<head>
    <title>New Task - PyPro Todo App</title>
    <link rel="stylesheet" href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css">
</head>
<body data-bs-theme="dark">
    <div class="container py-4">
        <h1 class="mb-4">New Task</h1>
        
        <form action="/tasks/new" method="post">
            <div class="mb-3">
                <label for="title" class="form-label">Title</label>
                <input type="text" class="form-control" id="title" name="title" required>
            </div>
            
            <div class="mb-3">
                <label for="description" class="form-label">Description</label>
                <textarea class="form-control" id="description" name="description" rows="3"></textarea>
            </div>
            
            <div class="mb-3">
                <button type="submit" class="btn btn-primary">Add Task</button>
                <a href="/" class="btn btn-secondary">Cancel</a>
            </div>
        </form>
    </div>
</body>
</html>
    '''
}

# Create template files at runtime
import os
templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)
    
for name, content in templates.items():
    template_path = os.path.join(templates_dir, name)
    if not os.path.exists(template_path):
        with open(template_path, 'w') as f:
            f.write(content)

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
