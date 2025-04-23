import os
import sys
import unittest
import tempfile

# Make sure pypro can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pypro import PyProApp, route, render_template, Response


class TestBasicFunctionality(unittest.TestCase):
    
    def setUp(self):
        # Create a test application
        self.app = PyProApp(__name__)
        
        # Add some routes
        @self.app.route('/')
        def index(request):
            return "Hello, World!"
            
        @self.app.route('/echo/<message>')
        def echo(request, message):
            return f"Echo: {message}"
            
        @self.app.route('/json')
        def json_route(request):
            return Response.json({"message": "Hello, JSON!"})
    
    def test_app_creation(self):
        """Test that app is created correctly."""
        self.assertIsInstance(self.app, PyProApp)
        self.assertEqual(self.app.import_name, '__main__')
    
    def test_routing(self):
        """Test that routes are registered correctly."""
        handler, params = self.app.router.match_route('/', 'GET')
        self.assertIsNotNone(handler)
        self.assertEqual(params, {})
        
        # Test route with parameter
        handler, params = self.app.router.match_route('/echo/test', 'GET')
        self.assertIsNotNone(handler)
        self.assertEqual(params, {'message': 'test'})
        
        # Test non-existent route
        handler, params = self.app.router.match_route('/not-found', 'GET')
        self.assertIsNone(handler)
    
    def test_response_creation(self):
        """Test response creation."""
        # Test string response
        response = Response("Hello")
        self.assertEqual(response.body, "Hello")
        self.assertEqual(response.status_code, 200)
        
        # Test JSON response
        response = Response.json({"message": "Hello"})
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        
        # Test redirect
        response = Response.redirect('/other')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/other')


class TestTemplateRendering(unittest.TestCase):
    
    def setUp(self):
        # Create a temp directory for templates
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # Create a test application
        self.app = PyProApp(__name__, template_folder=self.temp_dir.name)
        
        # Create a test template
        with open(os.path.join(self.temp_dir.name, 'test.html'), 'w') as f:
            f.write("<h1>Hello, {{ name }}!</h1>")
    
    def tearDown(self):
        self.temp_dir.cleanup()
    
    def test_render_template(self):
        """Test template rendering."""
        result = self.app.template_engine.render('test.html', name='PyPro')
        self.assertEqual(result, "<h1>Hello, PyPro!</h1>")


class TestSecurity(unittest.TestCase):
    
    def test_password_hashing(self):
        """Test password hashing and verification."""
        from pypro.security import generate_password_hash, check_password_hash
        
        password = "secure_password123"
        hashed = generate_password_hash(password)
        
        # Check that the hash is in the correct format
        self.assertTrue(hashed.startswith("pbkdf2:sha256$"))
        
        # Check that verification works
        self.assertTrue(check_password_hash(hashed, password))
        self.assertFalse(check_password_hash(hashed, "wrong_password"))
    
    def test_token_generation(self):
        """Test token generation and verification."""
        from pypro.security import create_token, verify_token
        
        data = {"user_id": 123, "role": "admin"}
        secret_key = "test_secret_key"
        
        token = create_token(data, secret_key)
        
        # Verify the token
        decoded = verify_token(token, secret_key)
        self.assertEqual(decoded, data)
        
        # Verify with wrong key
        decoded = verify_token(token, "wrong_key")
        self.assertIsNone(decoded)


if __name__ == '__main__':
    unittest.main()
