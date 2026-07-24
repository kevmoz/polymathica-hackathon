"""Olana Agent Core - Main conversational agent logic"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime


@dataclass
class Message:
    """Conversational message"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: str
    metadata: Dict[str, Any] = None


class OlanaAgent:
    """Conversational scientific agent for POLYMATHICA.
    
    Responsibilities:
    - Accept research questions in natural language
    - Maintain persistent conversation context
    - Provide experiment guidance and recommendations
    - Discuss results and suggest refinements
    - Learn from experimental outcomes
    """
    
    def __init__(self):
        self.conversation_history: List[Message] = []
        self.laboratory_context: Optional[Any] = None
        self.research_memory: Dict[str, Any] = {}
        
    def process_message(self, user_input: str) -> str:
        """Process user message and generate response.
        
        Args:
            user_input: User's natural language input
            
        Returns:
            Agent's response
            
        Example:
            >>> agent = OlanaAgent()
            >>> response = agent.process_message(
            ...     "Can you help me design a CFD simulation of channel flow?"
            ... )
            >>> print(response)
            "I'd be happy to help with your channel flow simulation..."
        """
        # Add user message to history
        user_msg = Message(
            role="user",
            content=user_input,
            timestamp=datetime.now().isoformat(),
        )
        self.conversation_history.append(user_msg)
        
        # Generate response (placeholder for now)
        response = self._generate_response(user_input)
        
        # Add assistant response to history
        assistant_msg = Message(
            role="assistant",
            content=response,
            timestamp=datetime.now().isoformat(),
        )
        self.conversation_history.append(assistant_msg)
        
        return response
    
    def _generate_response(self, user_input: str) -> str:
        """Generate response to user input.
        
        Args:
            user_input: User's input
            
        Returns:
            Generated response
        """
        # This will be replaced with actual LLM integration
        return (
            "I understand you're interested in scientific simulation. "
            "I can help you with:\n"
            "- Designing experiments\n"
            "- Setting up simulations\n"
            "- Analyzing results\n"
            "- Interpreting findings\n"
            "What would you like to explore?"
        )
    
    def get_conversation_history(self) -> List[Message]:
        """Get full conversation history.
        
        Returns:
            List of messages in conversation
        """
        return self.conversation_history.copy()
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history.clear()
