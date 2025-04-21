import argparse
import os
import sys
import importlib.util
import json
from typing import Dict, Any, Optional, List

from .app import create_app, FlaskMCP
from .config import Config


def load_module_from_path(module_path: str) -> Any:
    """
    Load a Python module from a file path.
    
    Args:
        module_path: Path to the Python module
        
    Returns:
        Loaded module or None if loading fails
    """
    try:
        module_name = os.path.basename(module_path).replace('.py', '')
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None:
            return None
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"Error loading module {module_path}: {e}")
        return None


def load_config_from_file(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from a file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dictionary containing configuration settings
    """
    if config_path.endswith('.json'):
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading JSON config from {config_path}: {e}")
            return {}
    
    elif config_path.endswith('.py'):
        try:
            module = load_module_from_path(config_path)
            if module and hasattr(module, 'config'):
                if isinstance(module.config, dict):
                    return module.config
                elif isinstance(module.config, Config):
                    # Convert Config object to dict
                    config_dict = {}
                    for key in dir(module.config):
                        if not key.startswith('_') and not callable(getattr(module.config, key)):
                            config_dict[key] = getattr(module.config, key)
                    return config_dict
            return {}
        except Exception as e:
            print(f"Error loading Python config from {config_path}: {e}")
            return {}
    
    else:
        print(f"Unsupported config file format: {config_path}")
        return {}


def main():
    """Entry point for the FlaskMCP CLI."""
    parser = argparse.ArgumentParser(description="FlaskMCP: A Flask-based Model Context Protocol implementation")
    
    # Server subcommand
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Server command
    server_parser = subparsers.add_parser('serve', help='Start a FlaskMCP server')
    server_parser.add_argument('--app', type=str, help='Path to a Python module containing a Flask app with FlaskMCP')
    server_parser.add_argument('--host', type=str, help='Host to bind the server to')
    server_parser.add_argument('--port', type=int, help='Port to bind the server to')
    server_parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    server_parser.add_argument('--config', type=str, help='Path to a configuration file (JSON or Python)')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Display information about FlaskMCP')
    
    # Version command
    version_parser = subparsers.add_parser('version', help='Display FlaskMCP version')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize a new FlaskMCP project')
    init_parser.add_argument('--dir', type=str, default='.', help='Directory to initialize the project in')
    
    args = parser.parse_args()
    
    # Handle commands
    if args.command == 'serve':
        # Load config from file if provided
        config = {}
        if args.config:
            config = load_config_from_file(args.config)
        
        # Override config with command line arguments
        if args.host:
            config['HOST'] = args.host
        if args.port:
            config['PORT'] = args.port
        if args.debug:
            config['DEBUG'] = True
        
        # If app path is provided, load and run that app
        if args.app:
            module = load_module_from_path(args.app)
            if module and hasattr(module, 'app'):
                app = module.app
                host = config.get('HOST', '127.0.0.1')
                port = config.get('PORT', 5000)
                debug = config.get('DEBUG', False)
                print(f"Starting FlaskMCP server with custom app at http://{host}:{port}")
                app.run(host=host, port=port, debug=debug)
            else:
                print(f"Error: Could not find Flask app in {args.app}")
                sys.exit(1)
        else:
            # Create a new app with the provided config
            app = create_app(config)
            host = config.get('HOST', '127.0.0.1')
            port = config.get('PORT', 5000)
            debug = config.get('DEBUG', False)
            print(f"Starting FlaskMCP server at http://{host}:{port}")
            app.run(host=host, port=port, debug=debug)
    
    elif args.command == 'info':
        # Display information about FlaskMCP
        config = Config()
        print("FlaskMCP: A Flask-based Model Context Protocol implementation")
        print(f"Version: {config.VERSION}")
        print("\nDefault Configuration:")
        print(config)
        
        print("\nInstalled at:", os.path.dirname(os.path.abspath(__file__)))
        
        print("\nAvailable Endpoints:")
        print(f"  GET    {config.MCP_PREFIX}/tools/list")
        print(f"  POST   {config.MCP_PREFIX}/tools/call")
        print(f"  GET    {config.MCP_PREFIX}/tools/schema/<tool_name>")
        print(f"  GET    {config.MCP_PREFIX}/resources/list")
        print(f"  GET    {config.MCP_PREFIX}/resources/<resource_id>")
        print(f"  POST   {config.MCP_PREFIX}/resources/")
        print(f"  PUT    {config.MCP_PREFIX}/resources/<resource_id>")
        print(f"  DELETE {config.MCP_PREFIX}/resources/<resource_id>")
        print(f"  GET    {config.MCP_PREFIX}/resources/<resource_id>/metadata")
        print(f"  GET    {config.MCP_PREFIX}/prompts/list")
        print(f"  GET    {config.MCP_PREFIX}/prompts/<prompt_id>")
        print(f"  POST   {config.MCP_PREFIX}/prompts/<prompt_id>/format")
        print(f"  POST   {config.MCP_PREFIX}/prompts/")
        print(f"  PUT    {config.MCP_PREFIX}/prompts/<prompt_id>")
        print(f"  DELETE {config.MCP_PREFIX}/prompts/<prompt_id>")
        if config.ENABLE_DOCS:
            print(f"  GET    {config.MCP_PREFIX}/docs")
            print(f"  GET    {config.MCP_PREFIX}/docs/openapi.json")
    
    elif args.command == 'version':
        # Display FlaskMCP version
        print(f"FlaskMCP v{Config.VERSION}")
    
    elif args.command == 'init':
        # Initialize a new FlaskMCP project
        project_dir = args.dir
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        
        # Create app.py
        app_path = os.path.join(project_dir, 'app.py')
        with open(app_path, 'w') as f:
            f.write("""# app.py

from flask import Flask, jsonify
from flaskmcp import create_app, tool, register_resource, register_prompt

# Create the Flask app with flaskMCP
app = create_app({'DEBUG': True})

# Register an example tool
@tool(name="add", description="Add two numbers")
def add(a: float, b: float) -> float:
    return a + b

# Register an example resource
register_resource(
    "greeting",
    "Welcome to FlaskMCP!",
    "A welcome message"
)

# Register an example prompt template
register_prompt(
    "greeting",
    "Hello, $name! Welcome to FlaskMCP.",
    "A personalized greeting"
)

# Add a custom route
@app.route('/')
def home():
    return jsonify({
        "message": "FlaskMCP Example App",
        "endpoints": {
            "tools": "/mcp/tools/list",
            "resources": "/mcp/resources/list",
            "prompts": "/mcp/prompts/list",
            "docs": "/mcp/docs"
        }
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
""")
        
        # Create requirements.txt
        req_path = os.path.join(project_dir, 'requirements.txt')
        with open(req_path, 'w') as f:
            f.write("flaskmcp>=0.1.0\n")
        
        # Create config.json
        config_path = os.path.join(project_dir, 'config.json')
        with open(config_path, 'w') as f:
            json.dump({
                "DEBUG": True,
                "HOST": "127.0.0.1",
                "PORT": 5000,
                "MCP_PREFIX": "/mcp",
                "ENABLE_DOCS": True
            }, f, indent=2)
        
        print(f"Initialized new FlaskMCP project in {os.path.abspath(project_dir)}")
        print("Files created:")
        print(f"  - {app_path}")
        print(f"  - {req_path}")
        print(f"  - {config_path}")
        print("\nTo run the app:")
        print(f"  cd {project_dir}")
        print("  pip install -r requirements.txt")
        print("  python app.py")
        print("\nOr use the flaskmcp CLI:")
        print(f"  flaskmcp serve --config config.json")
    
    else:
        # No command specified, show help
        parser.print_help()


if __name__ == "__main__":
    main()