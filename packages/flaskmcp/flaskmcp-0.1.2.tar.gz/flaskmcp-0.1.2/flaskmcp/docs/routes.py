
from flask import Blueprint, render_template, jsonify, request, current_app
import json
import os
import re
from ..core.tools import registry as tool_registry
from ..core.resources import registry as resource_registry
from ..core.prompts import registry as prompt_registry
from ..config import Config

# Create a blueprint for the documentation API
docs_bp = Blueprint('docs', __name__, template_folder='templates', static_folder='static')

@docs_bp.route('/', methods=['GET'])
def index():
    """
    Endpoint for API documentation home page.
    
    Returns:
        JSON response containing API documentation
    """
    # Get the base URL
    base_url = request.url_root.rstrip('/')
    mcp_prefix = current_app.config.get('MCP_PREFIX', Config.MCP_PREFIX)
    
    # Build documentation object
    docs = {
        "title": "FlaskMCP API Documentation",
        "version": current_app.config.get('VERSION', Config.VERSION),
        "description": "API documentation for the Flask-based Model Context Protocol (MCP)",
        "baseUrl": f"{base_url}{mcp_prefix}",
        "endpoints": {
            "tools": {
                "list": {
                    "method": "GET",
                    "path": f"{mcp_prefix}/tools/list",
                    "description": "List all available tools"
                },
                "call": {
                    "method": "POST",
                    "path": f"{mcp_prefix}/tools/call",
                    "description": "Call a tool by name with parameters",
                    "requestBody": {
                        "name": "string",
                        "params": "object"
                    }
                },
                "schema": {
                    "method": "GET",
                    "path": f"{mcp_prefix}/tools/schema/<tool_name>",
                    "description": "Get the schema for a tool"
                }
            },
            "resources": {
                "list": {
                    "method": "GET",
                    "path": f"{mcp_prefix}/resources/list",
                    "description": "List all available resources"
                },
                "get": {
                    "method": "GET",
                    "path": f"{mcp_prefix}/resources/<resource_id>",
                    "description": "Get a resource by ID"
                },
                "create": {
                    "method": "POST",
                    "path": f"{mcp_prefix}/resources/",
                    "description": "Create a new resource",
                    "requestBody": {
                        "id": "string",
                        "content": "any",
                        "description": "string (optional)",
                        "content_type": "string (optional)"
                    }
                },
                "update": {
                    "method": "PUT",
                    "path": f"{mcp_prefix}/resources/<resource_id>",
                    "description": "Update a resource",
                    "requestBody": {
                        "content": "any",
                        "description": "string (optional)"
                    }
                },
                "delete": {
                    "method": "DELETE",
                    "path": f"{mcp_prefix}/resources/<resource_id>",
                    "description": "Delete a resource"
                },
                "metadata": {
                    "method": "GET",
                    "path": f"{mcp_prefix}/resources/<resource_id>/metadata",
                    "description": "Get metadata for a resource"
                }
            },
            "prompts": {
                "list": {
                    "method": "GET",
                    "path": f"{mcp_prefix}/prompts/list",
                    "description": "List all available prompt templates"
                },
                "get": {
                    "method": "GET",
                    "path": f"{mcp_prefix}/prompts/<prompt_id>",
                    "description": "Get a prompt template by ID"
                },
                "format": {
                    "method": "POST",
                    "path": f"{mcp_prefix}/prompts/<prompt_id>/format",
                    "description": "Format a prompt template with variables",
                    "requestBody": {
                        "variable_name": "variable_value"
                    }
                },
                "create": {
                    "method": "POST",
                    "path": f"{mcp_prefix}/prompts/",
                    "description": "Create a new prompt template",
                    "requestBody": {
                        "id": "string",
                        "template": "string",
                        "description": "string (optional)"
                    }
                },
                "update": {
                    "method": "PUT",
                    "path": f"{mcp_prefix}/prompts/<prompt_id>",
                    "description": "Update a prompt template",
                    "requestBody": {
                        "template": "string",
                        "description": "string (optional)"
                    }
                },
                "delete": {
                    "method": "DELETE",
                    "path": f"{mcp_prefix}/prompts/<prompt_id>",
                    "description": "Delete a prompt template"
                }
            }
        }
    }
    
    return jsonify(docs)

@docs_bp.route('/tools', methods=['GET'])
def list_tools_docs():
    """
    Endpoint for tool documentation.
    
    Returns:
        JSON response containing tool documentation
    """
    tools = tool_registry.list_tools()
    
    return jsonify({
        "title": "Available Tools",
        "count": len(tools),
        "tools": tools
    })

@docs_bp.route('/resources', methods=['GET'])
def list_resources_docs():
    """
    Endpoint for resource documentation.
    
    Returns:
        JSON response containing resource documentation
    """
    resources = resource_registry.list_resources()
    
    return jsonify({
        "title": "Available Resources",
        "count": len(resources),
        "resources": resources
    })

@docs_bp.route('/prompts', methods=['GET'])
def list_prompts_docs():
    """
    Endpoint for prompt template documentation.
    
    Returns:
        JSON response containing prompt template documentation
    """
    prompts = prompt_registry.list_prompts()
    
    return jsonify({
        "title": "Available Prompt Templates",
        "count": len(prompts),
        "prompts": prompts
    })

@docs_bp.route('/openapi.json', methods=['GET'])
def openapi_spec():
    """
    Endpoint for OpenAPI specification.
    
    Returns:
        JSON response containing OpenAPI specification
    """
    base_url = request.url_root.rstrip('/')
    mcp_prefix = current_app.config.get('MCP_PREFIX', Config.MCP_PREFIX)
    
    # Build a simplified OpenAPI spec
    openapi = {
        "openapi": "3.0.0",
        "info": {
            "title": "FlaskMCP API",
            "description": "Flask-based Model Context Protocol (MCP) API",
            "version": current_app.config.get('VERSION', Config.VERSION)
        },
        "servers": [
            {
                "url": f"{base_url}{mcp_prefix}",
                "description": "FlaskMCP server"
            }
        ],
        "paths": {},
        "components": {
            "schemas": {
                "ToolCall": {
                    "type": "object",
                    "required": ["name", "params"],
                    "properties": {
                        "name": {"type": "string"},
                        "params": {"type": "object"}
                    }
                },
                "Resource": {
                    "type": "object",
                    "required": ["id", "content"],
                    "properties": {
                        "id": {"type": "string"},
                        "content": {"type": "object"},
                        "description": {"type": "string"},
                        "content_type": {"type": "string"}
                    }
                },
                "Prompt": {
                    "type": "object",
                    "required": ["id", "template"],
                    "properties": {
                        "id": {"type": "string"},
                        "template": {"type": "string"},
                        "description": {"type": "string"}
                    }
                }
            }
        }
    }
    
    # Add paths for tools
    openapi["paths"]["/tools/list"] = {
        "get": {
            "summary": "List all available tools",
            "responses": {
                "200": {
                    "description": "List of available tools",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "tools": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "name": {"type": "string"},
                                                "description": {"type": "string"},
                                                "schema": {"type": "object"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    openapi["paths"]["/tools/call"] = {
        "post": {
            "summary": "Call a tool by name with parameters",
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ToolCall"}
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "Tool execution result",
                    "content": {
                        "application/json": {
                            "schema": {
                                "oneOf": [
                                    {
                                        "type": "object",
                                        "properties": {
                                            "result": {"type": "object"},
                                            "timestamp": {"type": "number"}
                                        }
                                    },
                                    {
                                        "type": "object",
                                        "properties": {
                                            "error": {"type": "string"},
                                            "timestamp": {"type": "number"}
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        }
    }
    
    # Add some paths for resources and prompts (simplified for brevity)
    openapi["paths"]["/resources/list"] = {
        "get": {
            "summary": "List all available resources",
            "responses": {
                "200": {
                    "description": "List of available resources"
                }
            }
        }
    }
    
    openapi["paths"]["/prompts/list"] = {
        "get": {
            "summary": "List all available prompt templates",
            "responses": {
                "200": {
                    "description": "List of available prompt templates"
                }
            }
        }
    }
    
    return jsonify(openapi)