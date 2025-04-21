
from typing import Dict, Any, List, Optional, Callable, TypeVar, Type
import threading
import time
import json

__all__ = ["ResourceRegistry", "register_resource", "registry"]

T = TypeVar('T')

class Resource:
    """Represents a registered resource."""
    
    def __init__(
        self, 
        resource_id: str, 
        content: Any, 
        description: str = "",
        content_type: str = "application/json"
    ):
        """
        Initialize a resource.
        
        Args:
            resource_id: ID of the resource
            content: Content of the resource
            description: Description of the resource
            content_type: MIME type of the content
        """
        self.id = resource_id
        self.content = content
        self.description = description
        self.content_type = content_type
        self.created_at = time.time()
        self.updated_at = time.time()
    
    def update(self, content: Any, description: Optional[str] = None) -> None:
        """
        Update the resource content and optionally description.
        
        Args:
            content: New content for the resource
            description: New description for the resource
        """
        self.content = content
        if description is not None:
            self.description = description
        self.updated_at = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the resource to a dictionary.
        
        Returns:
            Dictionary representation of the resource
        """
        return {
            "id": self.id,
            "description": self.description,
            "content_type": self.content_type,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "content": self.content
        }


class ResourceRegistry:
    """Registry for MCP resources."""
    
    def __init__(self):
        """Initialize the resource registry."""
        self.resources: Dict[str, Resource] = {}
        self._lock = threading.RLock()
    
    def register(
        self, 
        resource_id: str, 
        content: Any, 
        description: str = "",
        content_type: str = "application/json"
    ) -> Resource:
        """
        Register a resource with the registry.
        
        Args:
            resource_id: ID of the resource
            content: Content of the resource
            description: Description of the resource
            content_type: MIME type of the content
            
        Returns:
            Registered Resource object
        """
        with self._lock:
            resource = Resource(resource_id, content, description, content_type)
            self.resources[resource_id] = resource
            return resource
    
    def get_resource(self, resource_id: str) -> Optional[Resource]:
        """
        Get a resource by ID.
        
        Args:
            resource_id: ID of the resource to retrieve
            
        Returns:
            Resource object or None if not found
        """
        with self._lock:
            return self.resources.get(resource_id)
    
    def list_resources(self) -> List[Dict[str, Any]]:
        """
        List all registered resources.
        
        Returns:
            List of resource dictionaries
        """
        with self._lock:
            return [
                {
                    "id": resource.id,
                    "description": resource.description,
                    "content_type": resource.content_type,
                    "created_at": resource.created_at,
                    "updated_at": resource.updated_at
                }
                for resource in self.resources.values()
            ]
    
    def update_resource(
        self, 
        resource_id: str, 
        content: Any, 
        description: Optional[str] = None
    ) -> Optional[Resource]:
        """
        Update a resource.
        
        Args:
            resource_id: ID of the resource to update
            content: New content for the resource
            description: New description for the resource
            
        Returns:
            Updated Resource object or None if not found
        """
        with self._lock:
            resource = self.get_resource(resource_id)
            if resource:
                resource.update(content, description)
            return resource
    
    def deregister(self, resource_id: str) -> bool:
        """
        Deregister a resource.
        
        Args:
            resource_id: ID of the resource to deregister
            
        Returns:
            True if deregistered, False if not found
        """
        with self._lock:
            if resource_id in self.resources:
                del self.resources[resource_id]
                return True
            return False
    
    def save_to_file(self, file_path: str) -> None:
        """
        Save all resources to a file.
        
        Args:
            file_path: Path to save resources to
        """
        with self._lock:
            try:
                resources_data = {
                    resource_id: {
                        "id": resource.id,
                        "description": resource.description,
                        "content_type": resource.content_type,
                        "created_at": resource.created_at,
                        "updated_at": resource.updated_at,
                        "content": resource.content if resource.content_type == "application/json" else str(resource.content)
                    }
                    for resource_id, resource in self.resources.items()
                }
                
                with open(file_path, 'w') as f:
                    json.dump(resources_data, f, indent=2)
            except Exception as e:
                print(f"Error saving resources to file: {e}")
    
    def load_from_file(self, file_path: str) -> int:
        """
        Load resources from a file.
        
        Args:
            file_path: Path to load resources from
            
        Returns:
            Number of resources loaded
        """
        try:
            with open(file_path, 'r') as f:
                resources_data = json.load(f)
            
            with self._lock:
                for resource_id, resource_data in resources_data.items():
                    self.resources[resource_id] = Resource(
                        resource_id=resource_data["id"],
                        content=resource_data["content"],
                        description=resource_data["description"],
                        content_type=resource_data.get("content_type", "application/json")
                    )
                
                return len(resources_data)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading resources from file: {e}")
            return 0


# Create a global registry instance
registry = ResourceRegistry()


def register_resource(
    resource_id: str, 
    content: Any, 
    description: str = "",
    content_type: str = "application/json"
) -> Resource:
    """
    Register a resource with the registry.
    
    Args:
        resource_id: ID of the resource
        content: Content of the resource
        description: Description of the resource
        content_type: MIME type of the content
        
    Returns:
        Registered Resource object
    """
    return registry.register(resource_id, content, description, content_type)