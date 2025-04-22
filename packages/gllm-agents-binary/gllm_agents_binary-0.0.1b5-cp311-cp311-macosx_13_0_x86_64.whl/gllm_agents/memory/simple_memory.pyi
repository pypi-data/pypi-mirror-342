from gllm_agents.memory.base import BaseMemory as BaseMemory, ChatMessage as ChatMessage

class SimpleMemory(BaseMemory):
    """A simple memory implementation that stores messages in a list."""
    messages: list[ChatMessage]
    def __init__(self) -> None:
        """Initialize the SimpleMemory instance with an empty message list."""
    def add_message(self, role: str = '', content: str = ''):
        """Add a message to memory."""
    def get_messages(self) -> list[ChatMessage]:
        """Get all messages from memory."""
    def clear(self) -> None:
        """Clear all messages from memory."""
