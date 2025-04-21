# tests/test_resources.py

import unittest
import json
from flask import Flask
from flaskmcp.core.resources import resources_bp, registry, register_resource

class TestResources(unittest.TestCase):
    
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(resources_bp, url_prefix='/mcp')
        self.client = self.app.test_client()
        
        # Clear registry and register test resources
        registry.resources = {}
        
        register_resource("greeting", "Hello, world!", "A simple greeting")
        register_resource("data", {"name": "John", "age": 30}, "Sample user data")
    
    def test_list_resources(self):
        response = self.client.get('/mcp/resources/list')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('resources', data)
        
        resources = data['resources']
        self.assertEqual(len(resources), 2)
        
        resource_ids = [r['id'] for r in resources]
        self.assertIn('greeting', resource_ids)
        self.assertIn('data', resource_ids)
    
    def test_get_resource(self):
        response = self.client.get('/mcp/resources/greeting')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('resource', data)
        self.assertEqual(data['resource'], "Hello, world!")
    
    def test_get_nonexistent_resource(self):
        response = self.client.get('/mcp/resources/nonexistent')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)
        self.assertIn("not found", data['error'])

if __name__ == '__main__':
    unittest.main()
