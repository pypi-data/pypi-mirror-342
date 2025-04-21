
from typing import Dict, Any, List, Optional, Callable, TypeVar, Type, get_type_hints
import inspect
import functools
import json
import threading
import time
from ..schema import infer_schema_from_function

__all__ = ["ToolRegistry", "tool", "registry"]

T = TypeVar('T')

class ToolResult:
    """Represents the result of a tool execution."""
    
    def __init__(self, result: Any, error: Optional[str] = None):
        """
        Initialize a tool result.
        
        Args:
            result: Result of the tool execution
            error: Error message if execution failed
        """
        self.result = result
        self.error = error
        self.timestamp = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the result to a dictionary.
        
        Returns:
            Dictionary representation of the result
        """
        if self.error:
            return {
                "error": self.error,
                "timestamp": self.timestamp
            }
        return {
            "result": self.result,
            "timestamp": self.timestamp
        }


class Tool:
    """Represents a registered tool."""
    
    def __init__(
        self, 
        name: str, 
        function: Callable, 
        description: str = "", 
        schema: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a tool.
        
        Args:
            name: Name of the tool
            function: Function to execute
            description: Description of the tool
            schema: JSON schema for the tool parameters
        """
        self.name = name
        self.function = function
        self.description = description
        self.schema = schema or infer_schema_from_function(function)
        self.original_function = function
    
    def execute(self, params: Dict[str, Any]) -> ToolResult:
        """
        Execute the tool with the given parameters.
        
        Args:
            params: Parameters to pass to the tool function
            
        Returns:
            ToolResult object containing the result or error
        """
        try:
            result = self.function(**params)
            return ToolResult(result)
        except Exception as e:
            return ToolResult(None, str(e))
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the tool to a dictionary.
        
        Returns:
            Dictionary representation of the tool
        """
        return {
            "name": self.name,
            "description": self.description,
            "schema": self.schema,
            "function": self.original_function.__name__
        }


class ToolRegistry:
    """Registry for MCP tools."""
    
    def __init__(self):
        """Initialize the tool registry."""
        self.tools: Dict[str, Tool] = {}
        self._lock = threading.RLock()
    
    def register(
        self, 
        name: str, 
        func: Callable, 
        description: str = "",
        schema: Optional[Dict[str, Any]] = None
    ) -> Tool:
        """
        Register a tool function with the registry.
        
        Args:
            name: Name of the tool
            func: Function to register
            description: Description of the tool
            schema: JSON schema for the tool parameters
            
        Returns:
            Registered Tool object
        """
        with self._lock:
            tool = Tool(name, func, description, schema)
            self.tools[name] = tool
            return tool
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """
        Get a tool by name.
        
        Args:
            name: Name of the tool to retrieve
            
        Returns:
            Tool object or None if not found
        """
        with self._lock:
            return self.tools.get(name)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        List all registered tools.
        
        Returns:
            List of tool dictionaries
        """
        with self._lock:
            return [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "schema": tool.schema
                }
                for tool in self.tools.values()
            ]
    
    def call_tool(self, name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a tool by name with the given parameters.
        
        Args:
            name: Name of the tool to call
            params: Parameters to pass to the tool
            
        Returns:
            Dictionary containing the result or error
        """
        with self._lock:
            tool = self.get_tool(name)
            if not tool:
                return {"error": f"Tool '{name}' not found"}
            
            result = tool.execute(params)
            return result.to_dict()
    
    def deregister(self, name: str) -> bool:
        """
        Deregister a tool.
        
        Args:
            name: Name of the tool to deregister
            
        Returns:
            True if deregistered, False if not found
        """
        with self._lock:
            if name in self.tools:
                del self.tools[name]
                return True
            return False


# Create a global registry instance
registry = ToolRegistry()


def tool(name: Optional[str] = None, description: str = "", schema: Optional[Dict[str, Any]] = None):
    """
    Decorator to register a function as a tool.
    
    Args:
        name: Name of the tool (defaults to function name)
        description: Description of the tool
        schema: JSON schema for the tool parameters
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        nonlocal name
        tool_name = name or func.__name__
        
        # Register the tool
        registry.register(tool_name, func, description, schema)
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator