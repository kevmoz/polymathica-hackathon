"""Olana - Conversational Scientific Agent

Natural language interface to the POLYMATHICA laboratory.

Provides:
- Natural language experiment design and guidance
- Persistent conversation context
- Results discussion and interpretation
- Learning from experimental outcomes
"""

__version__ = "0.1.0"

from .agent import OlanaAgent
from .dialogue import DialogueManager, ConversationContext

__all__ = [
    "OlanaAgent",
    "DialogueManager",
    "ConversationContext",
]
