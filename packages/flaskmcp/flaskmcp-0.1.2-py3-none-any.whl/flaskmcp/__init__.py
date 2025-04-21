# flaskmcp/__init__.py

from .app import create_app, FlaskMCP
from .core.tools import tool, registry as tool_registry
from .core.resources import register_resource, registry as resource_registry
from .core.prompts import register_prompt, registry as prompt_registry
from .context.manager import ContextManager
from .config import Config

__version__ = Config.VERSION

__all__ = [
    "create_app",
    "FlaskMCP",
    "tool",
    "register_resource",
    "register_prompt",
    "ContextManager",
    "Config",
    "tool_registry",
    "resource_registry",
    "prompt_registry"
]

