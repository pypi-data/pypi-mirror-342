import json
import os
from typing import Dict, Any, Optional, List, Tuple, Union

def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    Load and parse a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Dictionary containing the parsed JSON
        
    Raises:
        FileNotFoundError: If the file does not exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(data: Dict[str, Any], file_path: str, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Data to save
        file_path: Path to save the file to
        indent: Number of spaces for indentation
        
    Raises:
        IOError: If the file cannot be written
    """
    # Create directory if it doesn't exist
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent)

def validate_params(
    params: Dict[str, Any], 
    required_params: Dict[str, type]
) -> Optional[str]:
    """
    Validate that params dictionary contains required parameters of specified types.
    
    Args:
        params: Parameters to validate
        required_params: Dictionary mapping parameter names to expected types
        
    Returns:
        Error message if validation fails, None otherwise
    """
    for param_name, param_type in required_params.items():
        if param_name not in params:
            return f"Missing required parameter: {param_name}"
        
        if not isinstance(params[param_name], param_type):
            actual_type = type(params[param_name]).__name__
            expected_type = param_type.__name__
            return f"Parameter '{param_name}' should be of type '{expected_type}', got '{actual_type}'"
    
    return None

def merge_dicts(
    *dicts: Dict[str, Any], 
    overwrite: bool = True
) -> Dict[str, Any]:
    """
    Merge multiple dictionaries into a single dictionary.
    
    Args:
        *dicts: Dictionaries to merge
        overwrite: Whether to overwrite keys or keep the first occurrence
        
    Returns:
        Merged dictionary
    """
    result = {}
    
    for d in dicts:
        for key, value in d.items():
            if key not in result or overwrite:
                result[key] = value
    
    return result

def to_snake_case(s: str) -> str:
    """
    Convert a string to snake_case.
    
    Args:
        s: String to convert
        
    Returns:
        Snake case string
    """
    import re
    s = re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()
    s = re.sub(r'[^a-zA-Z0-9]', '_', s)
    s = re.sub(r'_{2,}', '_', s)
    return s.strip('_')

def to_camel_case(s: str) -> str:
    """
    Convert a string to camelCase.
    
    Args:
        s: String to convert
        
    Returns:
        Camel case string
    """
    import re
    s = re.sub(r'[^a-zA-Z0-9]', ' ', s)
    words = s.split()
    if not words:
        return ''
    result = words[0].lower()
    for word in words[1:]:
        if word:
            result += word[0].upper() + word[1:].lower()
    return result

def format_datetime(timestamp: float, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Format a Unix timestamp as a date string.
    
    Args:
        timestamp: Unix timestamp
        format_str: Format string for strftime
        
    Returns:
        Formatted date string
    """
    from datetime import datetime
    return datetime.fromtimestamp(timestamp).strftime(format_str)

def deep_get(dictionary: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
    """
    Safely get a value from a nested dictionary.
    
    Args:
        dictionary: Dictionary to get value from
        keys: List of keys to traverse
        default: Default value to return if key not found
        
    Returns:
        Value at the specified path or default
    """
    current = dictionary
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

def is_json_serializable(obj: Any) -> bool:
    """
    Check if an object is JSON serializable.
    
    Args:
        obj: Object to check
        
    Returns:
        True if the object is JSON serializable, False otherwise
    """
    try:
        json.dumps(obj)
        return True
    except (TypeError, OverflowError):
        return False