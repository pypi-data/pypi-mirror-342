# flaskmcp/config.py

from typing import Dict, Any, Optional

class Config:
    """Configuration settings for flaskMCP."""
    
    # Version information
    VERSION = "0.1.0"
    
    # Default prefix for MCP endpoints
    MCP_PREFIX = "/mcp"
    
    # Default host and port for Flask server
    HOST = "127.0.0.1"
    PORT = 5000
    
    # Default debug mode
    DEBUG = False
    
    # Maximum allowed content size (in bytes)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    
    # Enable API documentation
    ENABLE_DOCS = True
    
    # Default timeout for tool execution (in seconds)
    TOOL_TIMEOUT = 30
    
    # Context settings
    CONTEXT_TTL = 3600  # Time-to-live for contexts in seconds (1 hour)
    CONTEXT_CLEANUP_INTERVAL = 300  # Cleanup interval in seconds (5 minutes)
    
    # Authentication settings
    REQUIRE_AUTH = False
    AUTH_TOKEN_HEADER = "X-API-Key"
    AUTH_TOKENS = []  # List of valid API tokens
    
    # CORS settings
    ALLOW_CORS = True
    CORS_ORIGINS = "*"
    
    # Proxy settings
    BEHIND_PROXY = False
    
    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        """
        Initialize the configuration with optional overrides.
        
        Args:
            config_dict: Dictionary of configuration overrides
        """
        if config_dict:
            self.update(config_dict)
    
    def update(self, config_dict: Dict[str, Any]) -> None:
        """
        Update configuration settings from a dictionary.
        
        Args:
            config_dict: Dictionary of configuration settings
        """
        for key, value in config_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def get_flask_config(self) -> Dict[str, Any]:
        """
        Get configuration dictionary for Flask app.
        
        Returns:
            Dictionary of Flask configuration settings
        """
        return {
            "DEBUG": self.DEBUG,
            "MAX_CONTENT_LENGTH": self.MAX_CONTENT_LENGTH,
        }
    
    def __str__(self) -> str:
        """
        Return a string representation of the configuration.
        
        Returns:
            String representation
        """
        attrs = [attr for attr in dir(self) if not attr.startswith('_') and not callable(getattr(self, attr))]
        config_str = "FlaskMCP Configuration:\n"
        for attr in attrs:
            value = getattr(self, attr)
            config_str += f"  {attr}: {value}\n"
        return config_str