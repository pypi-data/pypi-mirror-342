from flask import Blueprint, request, jsonify, current_app
from typing import Dict, Any, List, Optional
import json

from ..core.prompts import registry

# Create a blueprint for the prompts API
prompts_bp = Blueprint('prompts', __name__)

@prompts_bp.route('/list', methods=['GET'])
def list_prompts():
    """
    Endpoint to list all available prompt templates.
    
    Returns:
        JSON response containing the list of available prompt templates
    """
    return jsonify({"prompts": registry.list_prompts()})

@prompts_bp.route('/<prompt_id>', methods=['GET'])
def get_prompt(prompt_id):
    """
    Endpoint to get a prompt template by ID.
    
    Args:
        prompt_id: ID of the prompt template to retrieve
        
    Returns:
        JSON response containing the prompt template or error
    """
    prompt = registry.get_prompt(prompt_id)
    if not prompt:
        return jsonify({"error": f"Prompt '{prompt_id}' not found"}), 404
    
    return jsonify(prompt.to_dict())

@prompts_bp.route('/<prompt_id>/format', methods=['POST'])
def format_prompt(prompt_id):
    """
    Endpoint to format a prompt template with variables.
    
    Args:
        prompt_id: ID of the prompt template to format
        
    Returns:
        JSON response containing the formatted prompt or error
    """
    variables = request.get_json() or {}
    
    result = registry.format_prompt(prompt_id, variables)
    
    if "error" in result:
        return jsonify(result), 404
    
    return jsonify(result)

@prompts_bp.route('/<prompt_id>', methods=['PUT'])
def update_prompt(prompt_id):
    """
    Endpoint to update a prompt template.
    
    Args:
        prompt_id: ID of the prompt template to update
        
    Returns:
        JSON response indicating success or error
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    template = data.get('template')
    description = data.get('description')
    
    if not template:
        return jsonify({"error": "Template must be provided"}), 400
    
    prompt = registry.update_prompt(prompt_id, template, description)
    if not prompt:
        return jsonify({"error": f"Prompt '{prompt_id}' not found"}), 404
    
    return jsonify({
        "message": f"Prompt '{prompt_id}' updated successfully",
        "prompt": {
            "id": prompt.id,
            "description": prompt.description,
            "variables": prompt.variables
        }
    })

@prompts_bp.route('/<prompt_id>', methods=['DELETE'])
def delete_prompt(prompt_id):
    """
    Endpoint to delete a prompt template.
    
    Args:
        prompt_id: ID of the prompt template to delete
        
    Returns:
        JSON response indicating success or error
    """
    success = registry.deregister(prompt_id)
    if not success:
        return jsonify({"error": f"Prompt '{prompt_id}' not found"}), 404
    
    return jsonify({"message": f"Prompt '{prompt_id}' deleted successfully"})

@prompts_bp.route('/', methods=['POST'])
def create_prompt():
    """
    Endpoint to create a new prompt template.
    
    Returns:
        JSON response containing the created prompt template ID
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    prompt_id = data.get('id')
    template = data.get('template')
    description = data.get('description', '')
    
    if not prompt_id:
        return jsonify({"error": "Prompt ID must be provided"}), 400
    
    if not template:
        return jsonify({"error": "Template must be provided"}), 400
    
    # Check if prompt already exists
    if registry.get_prompt(prompt_id):
        return jsonify({"error": f"Prompt '{prompt_id}' already exists"}), 409
    
    prompt = registry.register(prompt_id, template, description)
    
    return jsonify({
        "message": f"Prompt '{prompt_id}' created successfully",
        "prompt": {
            "id": prompt.id,
            "description": prompt.description,
            "variables": prompt.variables
        }
    }), 201