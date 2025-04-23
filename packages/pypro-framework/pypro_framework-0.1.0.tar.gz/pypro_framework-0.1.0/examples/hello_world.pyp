from pypro import PyProApp, render_template

# Create the application
app = PyProApp(__name__)
app.config['DEBUG'] = True

# Define routes
@app.route('/')
def index(request):
    return render_template('index.html', title='Hello from PyPro!', 
                           message='Welcome to your first PyPro application.')

@app.route('/hello/<name>')
def hello(request, name):
    return f"<h1>Hello, {name}!</h1>"

@app.route('/api/greeting/<name>')
def api_greeting(request, name):
    return {'greeting': f'Hello, {name}!'}

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
