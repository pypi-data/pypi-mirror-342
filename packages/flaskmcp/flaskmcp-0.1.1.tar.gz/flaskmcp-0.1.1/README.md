# FlaskMCP

FlaskMCP is a Flask-based implementation of the Model Context Protocol (MCP), designed to standardize communication between language models and context providers.

## Features

- **Tool Registry**: Register Python functions as tools that can be called through the API
- **Resource Management**: Manage static and dynamic resources accessible to models
- **Prompt Templates**: Define, manage, and format prompt templates with variables
- **Context Management**: Track conversation context between multiple requests
- **API Documentation**: Auto-generated API documentation with OpenAPI support
- **Schema Validation**: Input and output validation using JSON Schema
- **Comprehensive Error Handling**: Detailed error messages and appropriate status codes

## Installation

### From PyPI

```bash
pip install flaskmcp
```

### From Source

```bash
git clone https://github.com/Vprashant/flaskmcp.git
cd flaskmcp
pip install -e .
```

## Quick Start

```python
from flask import Flask
from flaskmcp import create_app, tool, register_resource, register_prompt

# Create a Flask app with FlaskMCP
app = create_app({'DEBUG': True})

# Register a tool
@tool(name="add", description="Add two numbers")
def add(a: float, b: float) -> float:
    return a + b

# Register a resource
register_resource(
    "greeting",
    "Welcome to FlaskMCP!",
    "A welcome message"
)

# Register a prompt template
register_prompt(
    "greeting",
    "Hello, $name! Welcome to FlaskMCP.",
    "A personalized greeting"
)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
```

## API Endpoints

FlaskMCP exposes the following API endpoints:

### Tools

- `GET /mcp/tools/list`: List all available tools
- `POST /mcp/tools/call`: Call a tool by name with parameters
- `GET /mcp/tools/schema/<tool_name>`: Get the schema for a tool

### Resources

- `GET /mcp/resources/list`: List all available resources
- `GET /mcp/resources/<resource_id>`: Get a resource by ID
- `POST /mcp/resources/`: Create a new resource
- `PUT /mcp/resources/<resource_id>`: Update a resource
- `DELETE /mcp/resources/<resource_id>`: Delete a resource
- `GET /mcp/resources/<resource_id>/metadata`: Get metadata for a resource

### Prompts

- `GET /mcp/prompts/list`: List all available prompt templates
- `GET /mcp/prompts/<prompt_id>`: Get a prompt template by ID
- `POST /mcp/prompts/<prompt_id>/format`: Format a prompt template with variables
- `POST /mcp/prompts/`: Create a new prompt template
- `PUT /mcp/prompts/<prompt_id>`: Update a prompt template
- `DELETE /mcp/prompts/<prompt_id>`: Delete a prompt template

### Documentation

- `GET /mcp/docs`: API documentation
- `GET /mcp/docs/openapi.json`: OpenAPI specification

## Examples

### Register and Call a Tool

```python
from flaskmcp import tool, create_app

app = create_app()

@tool(name="multiply", description="Multiply two numbers")
def multiply(a: float, b: float) -> float:
    return a * b

if __name__ == '__main__':
    app.run()
```

To call this tool through the API:

```bash
curl -X POST http://localhost:5000/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name": "multiply", "params": {"a": 5, "b": 3}}'
```

### Managing Resources

```python
from flaskmcp import register_resource, create_app

app = create_app()

# Register a resource
register_resource(
    "user_data",
    {"name": "Alice", "email": "alice@example.com"},
    "User profile data"
)

if __name__ == '__main__':
    app.run()
```

To access this resource through the API:

```bash
curl -X GET http://localhost:5000/mcp/resources/user_data
```

### Working with Prompt Templates

```python
from flaskmcp import register_prompt, create_app

app = create_app()

# Register a prompt template
register_prompt(
    "email_template",
    """
    Subject: $subject
    
    Dear $name,
    
    $content
    
    Best regards,
    $sender
    """,
    "Email template with variables"
)

if __name__ == '__main__':
    app.run()
```

To format this prompt through the API:

```bash
curl -X POST http://localhost:5000/mcp/prompts/email_template/format \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Meeting Invitation",
    "name": "Bob",
    "content": "I would like to invite you to a meeting tomorrow at 2 PM.",
    "sender": "Alice"
  }'
```

## Context Management

FlaskMCP includes a context management system for tracking conversation state across multiple requests:

```python
from flaskmcp import create_app
from flaskmcp.context.manager import ContextManager

app = create_app()
context_manager = ContextManager()

# Create a new context
context = context_manager.create_context()
context_id = context.id

# Add messages to the context
context_manager.add_message(context_id, "user", "Hello, how are you?")
context_manager.add_message(context_id, "assistant", "I'm doing well, thank you!")

# Get all messages in the context
messages = context_manager.get_context(context_id).get_messages()
```

## Advanced Usage

For more advanced usage examples, check the `examples` directory in the repository.

## Configuration

FlaskMCP can be configured through the `Config` class:

```python
from flaskmcp import create_app, Config

custom_config = Config()
custom_config.DEBUG = True
custom_config.MCP_PREFIX = "/api/mcp"
custom_config.PORT = 8080

app = create_app(custom_config.__dict__)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.