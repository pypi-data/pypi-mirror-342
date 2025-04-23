from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import uuid
from .db import save_conversation, load_conversation, list_conversations, get_latest_conversation

@dataclass
class Conversation:
    """Class to store and manage conversation state and history."""
    
    model: str
    tools: Optional[List[str]] = None
    interactive_tools: bool = False
    streaming: bool = True
    model_messages: List[Dict[str, Any]] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    kwargs: Dict[str, Any] = field(default_factory=dict)
    output_type: str = "text"
    
    def add_message(self, message: Dict[str, Any]) -> None:
        """Add a message to the conversation history."""
        self.model_messages.append(message)
        self.save()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the conversation to a dictionary for serialization."""
        return {
            "model": self.model,
            "tools": self.tools,
            "interactive_tools": self.interactive_tools,
            "streaming": self.streaming,
            "model_messages": self.model_messages,
            "created_at": self.created_at,
            "kwargs": self.kwargs,
            "output_type": self.output_type
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Conversation':
        """Create a Conversation instance from a dictionary."""
        return cls(**data)

    def save(self) -> None:
        """Save the conversation to the database."""
        save_conversation(self.id, self.to_dict(), self.created_at, self.output_type)

    @classmethod
    def load(cls, conversation_id: str) -> Optional['Conversation']:
        """Load a conversation from the database by ID."""
        data = load_conversation(conversation_id)
        if data:
            return cls.from_dict(data)
        return None

    @classmethod
    def list_all(cls) -> List[Dict[str, Any]]:
        """List all conversations in the database."""
        return list_conversations()

    @classmethod
    def get_latest(cls, output_type: Optional[str] = None) -> Optional['Conversation']:
        """Get the most recent conversation from the database.
        
        Args:
            output_type: Optional filter by output type (text, image, audio)
        """
        data = get_latest_conversation(output_type=output_type)
        if data:
            conv = cls.from_dict(data)
            conv.id = data['id']  # Ensure we preserve the ID
            return conv
        return None

    @classmethod
    def get_latest_text(cls) -> Optional['Conversation']:
        """Get the most recent text conversation from the database."""
        return cls.get_latest(output_type='text')
