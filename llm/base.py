from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from schemas.llm.llm_message import BaseMessage

class BaseLLMClient(ABC):
    """Base class for all LLM providers"""
    
    def __init__(self, api_key: str, model: str, temperature: float = 0.7, max_tokens: Optional[int] = None):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    @abstractmethod
    async def generate(
        self,
        messages: list[BaseMessage],
        tools: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> str:
        """Generate text response from messages"""
        pass
    
    @abstractmethod
    async def stream_generate(
        self,
        messages: list[BaseMessage],
        tools: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        """Stream text response from messages"""
        pass
