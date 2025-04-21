
from flask import Blueprint, request, jsonify, Response, current_app
from typing import Dict, Any, List, Optional
import json

from ..core.resources import registry

# Create a blueprint for the resources API
resources_bp = Blueprint('resources', __name__)

@resources_bp.route('/list', methods=['GET'])
def list_resources():
    """
    Endpoint to list all available resources.
    
    Returns:
        JSON response containing the list of available resources
    """
    return jsonify({"resources": registry.list_resources()})

@resources_bp.route('/<resource_id>', methods=['GET'])
def get_resource(resource_id):
    """
    Endpoint to get a resource by ID.
    
    Args:
        resource_id: ID of the resource to retrieve
        
    Returns:
        Resource content or error if not found
    """
    resource = registry.get_resource(resource_id)
    if not resource:
        return jsonify({"error": f"Resource '{resource_id}' not found"}), 404
    
    # Handle different content types
    if resource.content_type.startswith('text/'):
        return Response(str(resource.content), mimetype=resource.content_type)
    elif resource.content_type == 'application/json':
        return jsonify({"resource": resource.content})
    else:
        return jsonify({"resource": str(resource.content)})

@resources_bp.route('/<resource_id>/metadata', methods=['GET'])
def get_resource_metadata(resource_id):
    """
    Endpoint to get metadata for a resource.
    
    Args:
        resource_id: ID of the resource
        
    Returns:
        JSON response containing resource metadata
    """
    resource = registry.get_resource(resource_id)
    if not resource:
        return jsonify({"error": f"Resource '{resource_id}' not found"}), 404
    
    return jsonify({
        "id": resource.id,
        "description": resource.description,
        "content_type": resource.content_type,
        "created_at": resource.created_at,
        "updated_at": resource.updated_at
    })

@resources_bp.route('/<resource_id>', methods=['PUT'])
def update_resource(resource_id):
    """
    Endpoint to update a resource.
    
    Args:
        resource_id: ID of the resource to update
        
    Returns:
        JSON response indicating success or error
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    content = data.get('content')
    description = data.get('description')
    
    if content is None:
        return jsonify({"error": "Content must be provided"}), 400
    
    resource = registry.update_resource(resource_id, content, description)
    if not resource:
        return jsonify({"error": f"Resource '{resource_id}' not found"}), 404
    
    return jsonify({"message": f"Resource '{resource_id}' updated successfully"})

@resources_bp.route('/<resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    """
    Endpoint to delete a resource.
    
    Args:
        resource_id: ID of the resource to delete
        
    Returns:
        JSON response indicating success or error
    """
    success = registry.deregister(resource_id)
    if not success:
        return jsonify({"error": f"Resource '{resource_id}' not found"}), 404
    
    return jsonify({"message": f"Resource '{resource_id}' deleted successfully"})

@resources_bp.route('/', methods=['POST'])
def create_resource():
    """
    Endpoint to create a new resource.
    
    Returns:
        JSON response containing the created resource ID
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    resource_id = data.get('id')
    content = data.get('content')
    description = data.get('description', '')
    content_type = data.get('content_type', 'application/json')
    
    if not resource_id:
        return jsonify({"error": "Resource ID must be provided"}), 400
    
    if content is None:
        return jsonify({"error": "Content must be provided"}), 400
    
    # Check if resource already exists
    if registry.get_resource(resource_id):
        return jsonify({"error": f"Resource '{resource_id}' already exists"}), 409
    
    resource = registry.register(resource_id, content, description, content_type)
    
    return jsonify({
        "message": f"Resource '{resource_id}' created successfully",
        "resource": {
            "id": resource.id,
            "description": resource.description,
            "content_type": resource.content_type
        }
    }), 201