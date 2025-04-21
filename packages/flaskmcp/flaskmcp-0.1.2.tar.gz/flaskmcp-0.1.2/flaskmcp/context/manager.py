from typing import Dict, Any, Optional, List, Union, Callable
import uuid
import time
import threading
import json
from dataclasses import dataclass, field, asdict

__all__ = ["ContextManager", "Context"]

@dataclass
class Message:
    """Represents a message in a conversation."""
    role: str
    content: str
    timestamp: float = field(default_factory=time.time)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return asdict(self)


@dataclass
class Context:
    """
    Represents a conversation context.
    
    This class stores the state of a conversation, including messages,
    metadata, and any additional context-specific information.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    messages: List[Message] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    ttl: Optional[int] = None  # Time-to-live in seconds
    
    def add_message(self, role: str, content: str) -> Message:
        """
        Add a message to the context.
        
        Args:
            role: Role of the message sender (e.g., "user", "assistant")
            content: Content of the message
            
        Returns:
            The created Message object
        """
        message = Message(role=role, content=content)
        self.messages.append(message)
        self.updated_at = time.time()
        return message
    
    def get_messages(self) -> List[Dict[str, Any]]:
        """
        Get all messages in the context.
        
        Returns:
            List of message dictionaries
        """
        return [msg.to_dict() for msg in self.messages]
    
    def update_metadata(self, metadata: Dict[str, Any]) -> None:
        """
        Update context metadata.
        
        Args:
            metadata: Metadata to update
        """
        self.metadata.update(metadata)
        self.updated_at = time.time()
    
    def is_expired(self) -> bool:
        """
        Check if the context has expired.
        
        Returns:
            True if the context has expired, False otherwise
        """
        if self.ttl is None:
            return False
        return (time.time() - self.updated_at) > self.ttl
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert context to dictionary.
        
        Returns:
            Dictionary representation of the context
        """
        return {
            "id": self.id,
            "messages": self.get_messages(),
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "ttl": self.ttl
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Context':
        """
        Create a Context object from a dictionary.
        
        Args:
            data: Dictionary to create Context from
            
        Returns:
            Context object
        """
        messages = [Message(**msg) for msg in data.get("messages", [])]
        
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            messages=messages,
            metadata=data.get("metadata", {}),
            created_at=data.get("created_at", time.time()),
            updated_at=data.get("updated_at", time.time()),
            ttl=data.get("ttl")
        )


class ContextManager:
    """
    Manages conversation contexts for the MCP.
    
    This class provides methods for creating, retrieving, updating,
    and deleting contexts, as well as handling context persistence
    and cleanup.
    """
    
    def __init__(self, ttl: Optional[int] = 3600, cleanup_interval: int = 300):
        """
        Initialize the ContextManager.
        
        Args:
            ttl: Default time-to-live for contexts in seconds (None for no expiration)
            cleanup_interval: Interval in seconds for cleaning up expired contexts
        """
        self.contexts: Dict[str, Context] = {}
        self.default_ttl = ttl
        self.cleanup_interval = cleanup_interval
        self._lock = threading.RLock()
        
        # Start cleanup thread if TTL is set
        if ttl is not None:
            self._start_cleanup_thread()
    
    def create_context(self, metadata: Optional[Dict[str, Any]] = None, ttl: Optional[int] = None) -> Context:
        """
        Create a new context.
        
        Args:
            metadata: Initial metadata for the context
            ttl: Time-to-live in seconds (overrides default)
            
        Returns:
            Created Context object
        """
        with self._lock:
            context = Context(
                metadata=metadata or {},
                ttl=ttl if ttl is not None else self.default_ttl
            )
            self.contexts[context.id] = context
            return context
    
    def get_context(self, context_id: str) -> Optional[Context]:
        """
        Get a context by ID.
        
        Args:
            context_id: ID of the context to retrieve
            
        Returns:
            Context object or None if not found
        """
        with self._lock:
            context = self.contexts.get(context_id)
            
            if context and context.is_expired():
                self.delete_context(context_id)
                return None
                
            return context
    
    def update_context(self, context_id: str, metadata: Optional[Dict[str, Any]] = None) -> Optional[Context]:
        """
        Update a context.
        
        Args:
            context_id: ID of the context to update
            metadata: Metadata to update
            
        Returns:
            Updated Context object or None if not found
        """
        with self._lock:
            context = self.get_context(context_id)
            if context and metadata:
                context.update_metadata(metadata)
            return context
    
    def delete_context(self, context_id: str) -> bool:
        """
        Delete a context.
        
        Args:
            context_id: ID of the context to delete
            
        Returns:
            True if deleted, False if not found
        """
        with self._lock:
            if context_id in self.contexts:
                del self.contexts[context_id]
                return True
            return False
    
    def add_message(self, context_id: str, role: str, content: str) -> Optional[Message]:
        """
        Add a message to a context.
        
        Args:
            context_id: ID of the context to add the message to
            role: Role of the message sender
            content: Content of the message
            
        Returns:
            Created Message object or None if context not found
        """
        with self._lock:
            context = self.get_context(context_id)
            if context:
                return context.add_message(role, content)
            return None
    
    def get_all_contexts(self) -> List[Context]:
        """
        Get all active contexts.
        
        Returns:
            List of active Context objects
        """
        with self._lock:
            active_contexts = []
            for context_id in list(self.contexts.keys()):
                context = self.get_context(context_id)
                if context:
                    active_contexts.append(context)
            return active_contexts
    
    def _cleanup_expired(self) -> int:
        """
        Clean up expired contexts.
        
        Returns:
            Number of contexts cleaned up
        """
        with self._lock:
            expired = []
            for context_id, context in self.contexts.items():
                if context.is_expired():
                    expired.append(context_id)
            
            for context_id in expired:
                self.delete_context(context_id)
            
            return len(expired)
    
    def _start_cleanup_thread(self) -> None:
        """Start a thread to periodically clean up expired contexts."""
        def cleanup_worker():
            while True:
                time.sleep(self.cleanup_interval)
                self._cleanup_expired()
        
        thread = threading.Thread(target=cleanup_worker, daemon=True)
        thread.start()
    
    def save_to_file(self, file_path: str) -> None:
        """
        Save all contexts to a file.
        
        Args:
            file_path: Path to save contexts to
        """
        with self._lock:
            contexts_data = {
                context_id: context.to_dict() 
                for context_id, context in self.contexts.items()
            }
            
            with open(file_path, 'w') as f:
                json.dump(contexts_data, f, indent=2)
    
    def load_from_file(self, file_path: str) -> int:
        """
        Load contexts from a file.
        
        Args:
            file_path: Path to load contexts from
            
        Returns:
            Number of contexts loaded
        """
        try:
            with open(file_path, 'r') as f:
                contexts_data = json.load(f)
            
            with self._lock:
                for context_id, context_data in contexts_data.items():
                    self.contexts[context_id] = Context.from_dict(context_data)
                
                return len(contexts_data)
        except (IOError, json.JSONDecodeError):
            return 0