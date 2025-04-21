# flaskmcp/app.py

from flask import Flask, jsonify, request
from werkzeug.middleware.proxy_fix import ProxyFix
from typing import Dict, Any, Optional, List, Union, Callable

from .config import Config
from .routes.tools import tools_bp
from .routes.resources import resources_bp
from .routes.prompts import prompts_bp
from .docs.routes import docs_bp
from .middleware.error_handlers import register_error_handlers
from .context.manager import ContextManager

__all__ = ["create_app", "FlaskMCP"]

class FlaskMCP:
    """
    Main FlaskMCP application class that manages the Model Context Protocol implementation.
    
    This class encapsulates the Flask application and provides methods for configuring
    and extending the MCP functionality.
    """
    
    def __init__(
        self, 
        app: Optional[Flask] = None, 
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the FlaskMCP application.
        
        Args:
            app: An existing Flask application, or None to create a new one
            config: Configuration dictionary to override defaults
        """
        self.config = Config()
        if config:
            self.config.update(config)
            
        self.app = app or self._create_app()
        self.context_manager = ContextManager()
        
        # Configure the application
        self._configure_app()
        self._register_blueprints()
        self._setup_middleware()
        self._register_error_handlers()
    
    def _create_app(self) -> Flask:
        """Create a new Flask application."""
        app = Flask(__name__)
        return app
    
    def _configure_app(self) -> None:
        """Configure the Flask application with settings from config."""
        self.app.config.update(self.config.get_flask_config())
        
        # Fix proxy headers if behind a proxy
        if self.config.BEHIND_PROXY:
            self.app.wsgi_app = ProxyFix(
                self.app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
            )
    
    def _register_blueprints(self) -> None:
        """Register all blueprints with the Flask application."""
        prefix = self.config.MCP_PREFIX
        
        # Register core API blueprints
        self.app.register_blueprint(tools_bp, url_prefix=f"{prefix}/tools")
        self.app.register_blueprint(resources_bp, url_prefix=f"{prefix}/resources")
        self.app.register_blueprint(prompts_bp, url_prefix=f"{prefix}/prompts")
        
        # Register documentation blueprint if enabled
        if self.config.ENABLE_DOCS:
            self.app.register_blueprint(docs_bp, url_prefix=f"{prefix}/docs")
        
        # Register root MCP endpoint
        @self.app.route(f"{prefix}/", methods=["GET"])
        def mcp_info():
            """Root MCP endpoint returning library info."""
            return jsonify({
                "name": "flaskMCP",
                "version": self.config.VERSION,
                "description": "Flask-based implementation of the Model Context Protocol"
            })
    
    def _setup_middleware(self) -> None:
        """Set up middleware for the Flask application."""
        pass  # Implement middleware setup if needed
    
    def _register_error_handlers(self) -> None:
        """Register custom error handlers."""
        register_error_handlers(self.app)
    
    def run(self, host: Optional[str] = None, port: Optional[int] = None, **kwargs) -> None:
        """
        Run the Flask application.
        
        Args:
            host: Host to bind the server to
            port: Port to bind the server to
            **kwargs: Additional keyword arguments to pass to app.run()
        """
        host = host or self.config.HOST
        port = port or self.config.PORT
        self.app.run(host=host, port=port, **kwargs)


def create_app(config: Optional[Dict[str, Any]] = None) -> Flask:
    """
    Create and configure a Flask application with MCP endpoints.
    
    Args:
        config: Configuration dictionary to override defaults
        
    Returns:
        Configured Flask application
    """
    mcp = FlaskMCP(config=config)
    return mcp.app