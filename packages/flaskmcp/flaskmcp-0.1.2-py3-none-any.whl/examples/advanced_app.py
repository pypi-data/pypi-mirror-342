
from flask import Flask, request, jsonify, render_template_string
import os
import math
import time
import random
import json
from typing import Dict, Any, List, Optional

# Import flaskMCP components
from flaskmcp import create_app, tool, register_resource, register_prompt
from flaskmcp.core.tools import registry as tool_registry
from flaskmcp.core.resources import registry as resource_registry
from flaskmcp.core.prompts import registry as prompt_registry
from flaskmcp.context.manager import ContextManager

# Create the Flask app with flaskMCP
app = create_app({
    'DEBUG': True,
    'HOST': '0.0.0.0',
    'PORT': 5000
})

# Create a context manager for conversation tracking
context_manager = ContextManager(ttl=3600)

# Register examples tools
@tool(name="add", description="Add two numbers")
def add(a: float, b: float) -> float:
    """
    Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of the two numbers
    """
    return a + b

@tool(name="subtract", description="Subtract second number from first")
def subtract(a: float, b: float) -> float:
    """
    Subtract the second number from the first.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Difference between the two numbers
    """
    return a - b

@tool(name="multiply", description="Multiply two numbers")
def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Product of the two numbers
    """
    return a * b

@tool(name="divide", description="Divide first number by second")
def divide(a: float, b: float) -> float:
    """
    Divide the first number by the second.
    
    Args:
        a: First number (dividend)
        b: Second number (divisor)
        
    Returns:
        Quotient of the division
        
    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

@tool(name="calculate_distance", description="Calculate distance between two points")
def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Calculate the Euclidean distance between two points.
    
    Args:
        x1: X-coordinate of first point
        y1: Y-coordinate of first point
        x2: X-coordinate of second point
        y2: Y-coordinate of second point
        
    Returns:
        Euclidean distance between the points
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

@tool(name="weather_forecast", description="Get weather forecast for a location")
def weather_forecast(location: str, days: int = 3) -> List[Dict[str, Any]]:
    """
    Get a simulated weather forecast for a location.
    
    Args:
        location: Name of the location
        days: Number of days to forecast
        
    Returns:
        List of weather forecasts for each day
    """
    # Seed the random generator with the location name for consistent results
    random.seed(sum(ord(c) for c in location))
    
    weather_types = ["sunny", "partly cloudy", "cloudy", "rainy", "stormy", "snowy"]
    forecasts = []
    
    for day in range(days):
        temp_min = random.randint(10, 30)
        temp_max = temp_min + random.randint(3, 10)
        weather = random.choice(weather_types)
        humidity = random.randint(30, 90)
        wind_speed = random.randint(0, 30)
        
        forecasts.append({
            "day": day + 1,
            "temperature": {
                "min": temp_min,
                "max": temp_max,
                "unit": "celsius"
            },
            "weather": weather,
            "humidity": humidity,
            "wind_speed": wind_speed
        })
    
    return forecasts

# Register some example resources
register_resource(
    "greeting",
    "Welcome to the FlaskMCP advanced example application!",
    "A welcome message"
)

register_resource(
    "sample_data",
    {
        "users": [
            {"id": 1, "name": "Alice", "role": "admin"},
            {"id": 2, "name": "Bob", "role": "user"},
            {"id": 3, "name": "Charlie", "role": "user"}
        ],
        "products": [
            {"id": 101, "name": "Laptop", "price": 999.99},
            {"id": 102, "name": "Smartphone", "price": 499.99},
            {"id": 103, "name": "Headphones", "price": 149.99}
        ]
    },
    "Sample user and product data"
)

register_resource(
    "cities",
    [
        {"name": "New York", "country": "USA", "population": 8804190},
        {"name": "Tokyo", "country": "Japan", "population": 13929286},
        {"name": "London", "country": "UK", "population": 8982000},
        {"name": "Paris", "country": "France", "population": 2161000},
        {"name": "Sydney", "country": "Australia", "population": 5367800}
    ],
    "Sample city data"
)

# Register some example prompt templates
register_prompt(
    "greeting",
    "Hello, $name! Welcome to the FlaskMCP advanced example.",
    "A personalized greeting"
)

register_prompt(
    "weather_report",
    """Weather Report for $location

Today's Forecast:
- Temperature: $temperature°C
- Conditions: $conditions
- Humidity: $humidity%
- Wind: $wind km/h

Have a great day!""",
    "A template for weather reports"
)

register_prompt(
    "code_review",
    """Code Review: $title

Language: $language

```$language
$code
```

Feedback:
1. $point1
2. $point2
3. $point3

Overall: $summary""",
    "A template for code review reports"
)

# Custom routes

@app.route('/')
def home():
    """Home page with links to the MCP endpoints."""
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>FlaskMCP Advanced Example</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                }
                h2 {
                    color: #555;
                    margin-top: 30px;
                }
                ul {
                    list-style-type: none;
                    padding-left: 0;
                }
                li {
                    margin-bottom: 10px;
                }
                a {
                    color: #0066cc;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
                .endpoint {
                    background-color: #f8f8f8;
                    padding: 10px;
                    border-radius: 5px;
                    border-left: 4px solid #0066cc;
                }
                .method {
                    display: inline-block;
                    font-weight: bold;
                    width: 60px;
                }
            </style>
        </head>
        <body>
            <h1>FlaskMCP Advanced Example</h1>
            <p>Welcome to the FlaskMCP advanced example application. This application demonstrates how to use the FlaskMCP library to implement the Model Context Protocol.</p>
            
            <h2>MCP Endpoints</h2>
            <p>The following MCP endpoints are available:</p>
            
            <h3>Tools</h3>
            <ul>
                <li class="endpoint"><span class="method">GET</span> <a href="/mcp/tools/list">/mcp/tools/list</a> - List all available tools</li>
                <li class="endpoint"><span class="method">POST</span> <a href="javascript:void(0)">/mcp/tools/call</a> - Call a tool by name with parameters</li>
                <li class="endpoint"><span class="method">GET</span> <a href="/mcp/tools/schema/add">/mcp/tools/schema/add</a> - Get the schema for the 'add' tool</li>
            </ul>
            
            <h3>Resources</h3>
            <ul>
                <li class="endpoint"><span class="method">GET</span> <a href="/mcp/resources/list">/mcp/resources/list</a> - List all available resources</li>
                <li class="endpoint"><span class="method">GET</span> <a href="/mcp/resources/greeting">/mcp/resources/greeting</a> - Get the 'greeting' resource</li>
                <li class="endpoint"><span class="method">GET</span> <a href="/mcp/resources/sample_data">/mcp/resources/sample_data</a> - Get the 'sample_data' resource</li>
                <li class="endpoint"><span class="method">GET</span> <a href="/mcp/resources/cities">/mcp/resources/cities</a> - Get the 'cities' resource</li>
            </ul>
            
            <h3>Prompts</h3>
            <ul>
                <li class="endpoint"><span class="method">GET</span> <a href="/mcp/prompts/list">/mcp/prompts/list</a> - List all available prompt templates</li>
                <li class="endpoint"><span class="method">GET</span> <a href="/mcp/prompts/greeting">/mcp/prompts/greeting</a> - Get the 'greeting' prompt template</li>
                <li class="endpoint"><span class="method">POST</span> <a href="javascript:void(0)">/mcp/prompts/greeting/format</a> - Format the 'greeting' prompt template</li>
            </ul>
            
            <h3>Documentation</h3>
            <ul>
                <li class="endpoint"><span class="method">GET</span> <a href="/mcp/docs">/mcp/docs</a> - API documentation</li>
                <li class="endpoint"><span class="method">GET</span> <a href="/mcp/docs/openapi.json">/mcp/docs/openapi.json</a> - OpenAPI specification</li>
            </ul>
            
            <h2>Test the API</h2>
            <p>You can use tools like <a href="https://www.postman.com/" target="_blank">Postman</a> or <a href="https://curl.se/" target="_blank">curl</a> to test the API endpoints.</p>
            
            <h3>Example API calls:</h3>
            <pre>
# List all tools
curl -X GET http://localhost:5000/mcp/tools/list

# Call a tool
curl -X POST http://localhost:5000/mcp/tools/call \\
  -H "Content-Type: application/json" \\
  -d '{"name": "add", "params": {"a": 5, "b": 3}}'

# Format a prompt
curl -X POST http://localhost:5000/mcp/prompts/greeting/format \\
  -H "Content-Type: application/json" \\
  -d '{"name": "Alice"}'
            </pre>
        </body>
        </html>
    ''')

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    API endpoint for chatting with the context-aware MCP.
    
    This endpoint demonstrates how to use the context manager to track conversations
    and maintain state across multiple requests.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    context_id = data.get('context_id')
    message = data.get('message')
    
    if not message:
        return jsonify({"error": "Message must be provided"}), 400
    
    # Get or create context
    if context_id:
        context = context_manager.get_context(context_id)
        if not context:
            return jsonify({"error": f"Context '{context_id}' not found"}), 404
    else:
        context = context_manager.create_context()
        context_id = context.id
    
    # Add user message to context
    context_manager.add_message(context_id, "user", message)
    
    # Process the message (in a real application, this would involve LLM processing)
    response = "This is a simple echo response: " + message
    
    # Add assistant message to context
    context_manager.add_message(context_id, "assistant", response)
    
    return jsonify({
        "context_id": context_id,
        "response": response,
        "messages": context.get_messages()
    })

@app.route('/api/contexts', methods=['GET'])
def list_contexts():
    """API endpoint to list all active contexts."""
    contexts = context_manager.get_all_contexts()
    
    return jsonify({
        "contexts": [context.to_dict() for context in contexts]
    })

@app.route('/api/context/<context_id>', methods=['GET'])
def get_context(context_id):
    """API endpoint to get a specific context."""
    context = context_manager.get_context(context_id)
    if not context:
        return jsonify({"error": f"Context '{context_id}' not found"}), 404
    
    return jsonify(context.to_dict())

@app.route('/api/context/<context_id>', methods=['DELETE'])
def delete_context(context_id):
    """API endpoint to delete a specific context."""
    success = context_manager.delete_context(context_id)
    if not success:
        return jsonify({"error": f"Context '{context_id}' not found"}), 404
    
    return jsonify({"message": f"Context '{context_id}' deleted successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)