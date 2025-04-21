# tests/test_prompts.py

import unittest
import json
from flask import Flask
from flaskmcp.core.prompts import prompts_bp, registry, register_prompt

class TestPrompts(unittest.TestCase):
    
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(prompts_bp, url_prefix='/mcp')
        self.client = self.app.test_client()
        
        # Clear registry and register test prompts
        registry.prompts = {}
        
        register_prompt(
            "greeting",
            "Hello, $name! Welcome to $application.",
            "A customizable greeting"
        )
        register_prompt(
            "review",
            "Please review the following $type:\n\n$content",
            "A template for review requests"
        )
    
    def test_list_prompts(self):
        response = self.client.get('/mcp/prompts/list')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('prompts', data)
        
        prompts = data['prompts']
        self.assertEqual(len(prompts), 2)
        
        prompt_ids = [p['id'] for p in prompts]
        self.assertIn('greeting', prompt_ids)
        self.assertIn('review', prompt_ids)
    
    def test_format_prompt(self):
        response = self.client.post(
            '/mcp/prompts/greeting',
            json={'name': 'Alice', 'application': 'flaskMCP'}
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('prompt', data)
        self.assertEqual(data['prompt'], "Hello, Alice! Welcome to flaskMCP.")
    
    def test_format_nonexistent_prompt(self):
        response = self.client.post(
            '/mcp/prompts/nonexistent',
            json={'name': 'Alice'}
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)
        self.assertIn("not found", data['error'])
    
    def test_format_prompt_missing_variables(self):
        response = self.client.post(
            '/mcp/prompts/greeting',
            json={'name': 'Alice'}
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('prompt', data)
        # Missing variables should be left as is with the $ sign
        self.assertEqual(data['prompt'], "Hello, Alice! Welcome to $application.")

if __name__ == '__main__':
    unittest.main()
