from flask import Flask, jsonify
from flaskmcp import create_app, tool, register_resource, register_prompt

# Create the Flask app with flaskMCP
app = create_app({'DEBUG': True})

# Register some example tools
@tool(name="add", description="Add two numbers")
def add(a, b):
    return a + b

@tool(name="subtract", description="Subtract second number from first")
def subtract(a, b):
    return a - b

@tool(name="multiply", description="Multiply two numbers")
def multiply(a, b):
    return a * b

@tool(name="divide", description="Divide first number by second")
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Register some example resources
register_resource(
    "greeting",
    "Welcome to the flaskMCP example application!",
    "A welcome message"
)

register_resource(
    "sample_data",
    {
        "users": [
            {"id": 1, "name": "Alice", "role": "admin"},
            {"id": 2, "name": "Bob", "role": "user"},
            {"id": 3, "name": "Charlie", "role": "user"}
        ]
    },
    "Sample user data"
)

# Register some example prompt templates
register_prompt(
    "greeting",
    "Hello, $name! Welcome to flaskMCP.",
    "A personalized greeting"
)

register_prompt(
    "code_review",
    """Please review the following $language code:

```$language
$code
```

Focus on:
1. Code style and best practices
2. Potential bugs or edge cases
3. Performance considerations""",
    "A template for code review requests"
)

# Add a custom route to the app
@app.route('/')
def home():
    return jsonify({
        "message": "flaskMCP Example Application",
        "description": "Demonstrates the functionality of flaskMCP",
        "mcp_endpoint": "/mcp/"
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
