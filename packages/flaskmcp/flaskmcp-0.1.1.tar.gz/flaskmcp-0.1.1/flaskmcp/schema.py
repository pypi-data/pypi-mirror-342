# flaskmcp/schema.py

import jsonschema
from typing import Dict, Any, Optional, List, Union, Callable, Type, TypeVar, get_type_hints
import inspect
import json
from functools import wraps
from flask import request, jsonify, Response, current_app

__all__ = ["Schema", "validate_request", "schema_to_json"]

T = TypeVar('T')

class ValidationError(Exception):
    """Exception raised for schema validation errors."""
    
    def __init__(self, message: str, errors: Optional[List[Dict[str, Any]]] = None):
        self.message = message
        self.errors = errors or []
        super().__init__(self.message)


class Schema:
    """
    Base schema class for validating data structures.
    
    This class provides functionality similar to Pydantic models but uses jsonschema
    for validation to avoid the dependency on Pydantic.
    """
    
    __schema__: Dict[str, Any] = {}
    
    def __init__(self, **data):
        """
        Initialize a Schema instance with data and validate it.
        
        Args:
            **data: Data to validate against the schema
        
        Raises:
            ValidationError: If validation fails
        """
        self.validate(data)
        for key, value in data.items():
            setattr(self, key, value)
    
    @classmethod
    def validate(cls, data: Dict[str, Any]) -> None:
        """
        Validate data against the schema.
        
        Args:
            data: Data to validate
        
        Raises:
            ValidationError: If validation fails
        """
        try:
            jsonschema.validate(instance=data, schema=cls.__schema__)
        except jsonschema.exceptions.ValidationError as e:
            raise ValidationError(str(e), [{"loc": e.path, "msg": e.message}])
    
    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """
        Create a Schema instance from a dictionary.
        
        Args:
            data: Dictionary to convert to a Schema instance
        
        Returns:
            Schema instance
        """
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Schema instance to a dictionary.
        
        Returns:
            Dictionary representation of the Schema instance
        """
        return {key: getattr(self, key) for key in self.__schema__.get("properties", {})}
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.to_dict()})"


def schema_to_json(schema_class: Type[Schema]) -> Dict[str, Any]:
    """
    Convert a Schema class to a JSON schema.
    
    Args:
        schema_class: Schema class to convert
    
    Returns:
        JSON schema dictionary
    """
    return schema_class.__schema__


def validate_request(schema_class: Type[Schema]):
    """
    Decorator to validate request JSON data against a schema.
    
    Args:
        schema_class: Schema class to validate against
    
    Returns:
        Decorated function
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                data = request.get_json()
                if data is None:
                    return jsonify({"error": "No JSON data provided"}), 400
                
                schema = schema_class.from_dict(data)
                return func(*args, **kwargs, validated_data=schema)
            except ValidationError as e:
                return jsonify({
                    "error": "Validation error",
                    "message": e.message,
                    "details": e.errors
                }), 400
        return wrapper
    return decorator


# Schema definitions for standard MCP objects

class ToolSchema(Schema):
    """Schema for tool objects."""
    
    __schema__ = {
        "type": "object",
        "required": ["name"],
        "properties": {
            "name": {"type": "string"},
            "description": {"type": "string"},
            "parameters": {"type": "object"}
        }
    }


class ToolCallSchema(Schema):
    """Schema for tool call requests."""
    
    __schema__ = {
        "type": "object",
        "required": ["name", "params"],
        "properties": {
            "name": {"type": "string"},
            "params": {"type": "object"}
        }
    }


class ResourceSchema(Schema):
    """Schema for resource objects."""
    
    __schema__ = {
        "type": "object",
        "required": ["id"],
        "properties": {
            "id": {"type": "string"},
            "description": {"type": "string"},
            "content": {"type": "object"}
        }
    }


class PromptSchema(Schema):
    """Schema for prompt objects."""
    
    __schema__ = {
        "type": "object",
        "required": ["id", "template"],
        "properties": {
            "id": {"type": "string"},
            "template": {"type": "string"},
            "description": {"type": "string"}
        }
    }


def infer_schema_from_function(func: Callable) -> Dict[str, Any]:
    """
    Infer a JSON schema from a function's type hints.
    
    Args:
        func: Function to infer schema from
    
    Returns:
        JSON schema dictionary
    """
    signature = inspect.signature(func)
    type_hints = get_type_hints(func)
    
    properties = {}
    required = []
    
    for param_name, param in signature.parameters.items():
        if param_name in type_hints:
            param_type = type_hints[param_name]
            
            # Handle basic types
            if param_type == str:
                properties[param_name] = {"type": "string"}
            elif param_type == int:
                properties[param_name] = {"type": "integer"}
            elif param_type == float:
                properties[param_name] = {"type": "number"}
            elif param_type == bool:
                properties[param_name] = {"type": "boolean"}
            elif param_type == list or getattr(param_type, "__origin__", None) == list:
                properties[param_name] = {"type": "array"}
            elif param_type == dict or getattr(param_type, "__origin__", None) == dict:
                properties[param_name] = {"type": "object"}
            else:
                # For complex types, just use "object"
                properties[param_name] = {"type": "object"}
            
            # Check if parameter is required
            if param.default == inspect.Parameter.empty:
                required.append(param_name)
    
    return {
        "type": "object",
        "properties": properties,
        "required": required
    }