
from typing import Dict, Any, List, Optional, Callable, TypeVar, Type
import threading
import time
import json
import string
import re

__all__ = ["PromptRegistry", "register_prompt", "registry"]

T = TypeVar('T')

class PromptTemplate:
    """Represents a registered prompt template."""
    
    def __init__(
        self, 
        prompt_id: str, 
        template: str, 
        description: str = ""
    ):
        """
        Initialize a prompt template.
        
        Args:
            prompt_id: ID of the prompt template
            template: Template string
            description: Description of the template
        """
        self.id = prompt_id
        self.template = template
        self.description = description
        self.created_at = time.time()
        self.updated_at = time.time()
        
        # Extract variables from the template
        self.variables = self._extract_variables(template)
    
    def _extract_variables(self, template: str) -> List[str]:
        """
        Extract variable names from the template.
        
        Args:
            template: Template string
            
        Returns:
            List of variable names
        """
        # Find all $var and ${var} patterns
        variables = set()
        
        # Match $var pattern (simple variables)
        simple_vars = re.findall(r'\$([a-zA-Z_][a-zA-Z0-9_]*)', template)
        variables.update(simple_vars)
        
        # Match ${var} pattern (braced variables)
        braced_vars = re.findall(r'\${([a-zA-Z_][a-zA-Z0-9_]*)}', template)
        variables.update(braced_vars)
        
        return list(variables)
    
    def format(self, variables: Dict[str, Any]) -> str:
        """
        Format the template with the given variables.
        
        Args:
            variables: Variables to substitute in the template
            
        Returns:
            Formatted string
        """
        # Use string.Template for variable substitution
        template = string.Template(self.template)
        return template.safe_substitute(variables)
    
    def update(self, template: str, description: Optional[str] = None) -> None:
        """
        Update the template and optionally its description.
        
        Args:
            template: New template string
            description: New description
        """
        self.template = template
        if description is not None:
            self.description = description
        self.updated_at = time.time()
        
        # Update variables
        self.variables = self._extract_variables(template)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the prompt template to a dictionary.
        
        Returns:
            Dictionary representation of the prompt template
        """
        return {
            "id": self.id,
            "template": self.template,
            "description": self.description,
            "variables": self.variables,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class PromptRegistry:
    """Registry for MCP prompt templates."""
    
    def __init__(self):
        """Initialize the prompt registry."""
        self.prompts: Dict[str, PromptTemplate] = {}
        self._lock = threading.RLock()
    
    def register(
        self, 
        prompt_id: str, 
        template: str, 
        description: str = ""
    ) -> PromptTemplate:
        """
        Register a prompt template with the registry.
        
        Args:
            prompt_id: ID of the prompt template
            template: Template string
            description: Description of the template
            
        Returns:
            Registered PromptTemplate object
        """
        with self._lock:
            prompt = PromptTemplate(prompt_id, template, description)
            self.prompts[prompt_id] = prompt
            return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[PromptTemplate]:
        """
        Get a prompt template by ID.
        
        Args:
            prompt_id: ID of the prompt template to retrieve
            
        Returns:
            PromptTemplate object or None if not found
        """
        with self._lock:
            return self.prompts.get(prompt_id)
    
    def list_prompts(self) -> List[Dict[str, Any]]:
        """
        List all registered prompt templates.
        
        Returns:
            List of prompt template dictionaries
        """
        with self._lock:
            return [
                {
                    "id": prompt.id,
                    "description": prompt.description,
                    "variables": prompt.variables
                }
                for prompt in self.prompts.values()
            ]
    
    def format_prompt(self, prompt_id: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a prompt template with the given variables.
        
        Args:
            prompt_id: ID of the prompt template to format
            variables: Variables to substitute in the template
            
        Returns:
            Dictionary containing the formatted prompt or error
        """
        with self._lock:
            prompt = self.get_prompt(prompt_id)
            if not prompt:
                return {"error": f"Prompt '{prompt_id}' not found"}
            
            try:
                formatted = prompt.format(variables)
                return {"prompt": formatted}
            except Exception as e:
                return {"error": str(e)}
    
    def update_prompt(
        self, 
        prompt_id: str, 
        template: str, 
        description: Optional[str] = None
    ) -> Optional[PromptTemplate]:
        """
        Update a prompt template.
        
        Args:
            prompt_id: ID of the prompt template to update
            template: New template string
            description: New description
            
        Returns:
            Updated PromptTemplate object or None if not found
        """
        with self._lock:
            prompt = self.get_prompt(prompt_id)
            if prompt:
                prompt.update(template, description)
            return prompt
    
    def deregister(self, prompt_id: str) -> bool:
        """
        Deregister a prompt template.
        
        Args:
            prompt_id: ID of the prompt template to deregister
            
        Returns:
            True if deregistered, False if not found
        """
        with self._lock:
            if prompt_id in self.prompts:
                del self.prompts[prompt_id]
                return True
            return False
    
    def save_to_file(self, file_path: str) -> None:
        """
        Save all prompt templates to a file.
        
        Args:
            file_path: Path to save prompt templates to
        """
        with self._lock:
            try:
                prompts_data = {
                    prompt_id: prompt.to_dict()
                    for prompt_id, prompt in self.prompts.items()
                }
                
                with open(file_path, 'w') as f:
                    json.dump(prompts_data, f, indent=2)
            except Exception as e:
                print(f"Error saving prompts to file: {e}")
    
    def load_from_file(self, file_path: str) -> int:
        """
        Load prompt templates from a file.
        
        Args:
            file_path: Path to load prompt templates from
            
        Returns:
            Number of prompt templates loaded
        """
        try:
            with open(file_path, 'r') as f:
                prompts_data = json.load(f)
            
            with self._lock:
                for prompt_id, prompt_data in prompts_data.items():
                    self.prompts[prompt_id] = PromptTemplate(
                        prompt_id=prompt_data["id"],
                        template=prompt_data["template"],
                        description=prompt_data["description"]
                    )
                
                return len(prompts_data)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading prompts from file: {e}")
            return 0


# Create a global registry instance
registry = PromptRegistry()


def register_prompt(
    prompt_id: str, 
    template: str, 
    description: str = ""
) -> PromptTemplate:
    """
    Register a prompt template with the registry.
    
    Args:
        prompt_id: ID of the prompt template
        template: Template string
        description: Description of the template
        
    Returns:
        Registered PromptTemplate object
    """
    return registry.register(prompt_id, template, description)