from flask import Blueprint, request, jsonify, current_app
from typing import Dict, Any, List, Optional
import json

from ..core.tools import registry
from ..schema import validate_request, ToolCallSchema

# Create a blueprint for the tools API
tools_bp = Blueprint('tools', __name__)

@tools_bp.route('/list', methods=['GET'])
def list_tools():
    """
    Endpoint to list all available tools.
    
    Returns:
        JSON response containing the list of available tools
    """
    return jsonify({"tools": registry.list_tools()})

@tools_bp.route('/call', methods=['POST'])
@validate_request(ToolCallSchema)
def call_tool(validated_data):
    """
    Endpoint to call a tool by name with parameters.
    
    Args:
        validated_data: Validated request data
        
    Returns:
        JSON response containing the result or error
    """
    tool_name = validated_data.name
    params = validated_data.params
    
    result = registry.call_tool(tool_name, params)
    return jsonify(result)

@tools_bp.route('/schema/<tool_name>', methods=['GET'])
def get_tool_schema(tool_name):
    """
    Endpoint to get the schema for a tool.
    
    Args:
        tool_name: Name of the tool
        
    Returns:
        JSON schema for the tool or error if not found
    """
    tool = registry.get_tool(tool_name)
    if not tool:
        return jsonify({"error": f"Tool '{tool_name}' not found"}), 404
    
    return jsonify({"name": tool.name, "schema": tool.schema})