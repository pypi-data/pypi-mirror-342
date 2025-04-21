# tests/test_tools.py

import unittest
import json
from flask import Flask
from flaskmcp.core.tools import tools_bp, registry, tool

class TestTools(unittest.TestCase):
    
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(tools_bp, url_prefix='/mcp')
        self.client = self.app.test_client()
        
        # Clear registry and register test tools
        registry.tools = {}
        
        @tool(name="add", description="Add two numbers")
        def add(a, b):
            return a + b
        
        @tool(name="multiply", description="Multiply two numbers")
        def multiply(a, b):
            return a * b
    
    def test_list_tools(self):
        response = self.client.get('/mcp/tools/list')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('tools', data)
        
        tools = data['tools']
        self.assertEqual(len(tools), 2)
        
        tool_names = [t['name'] for t in tools]
        self.assertIn('add', tool_names)
        self.assertIn('multiply', tool_names)
    
    def test_call_tool(self):
        response = self.client.post(
            '/mcp/tools/call',
            json={'name': 'add', 'params': {'a': 5, 'b': 3}}
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('result', data)
        self.assertEqual(data['result'], 8)
    
    def test_call_nonexistent_tool(self):
        response = self.client.post(
            '/mcp/tools/call',
            json={'name': 'divide', 'params': {'a': 10, 'b': 2}}
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', data)
        self.assertIn("not found", data['error'])
    
    def test_call_tool_missing_params(self):
        response = self.client.post(
            '/mcp/tools/call',
            json={'name': 'add', 'params': {'a': 5}}
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
