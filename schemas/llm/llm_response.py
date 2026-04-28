from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class TokenUsage(BaseModel):
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    reasoning_tokens: Optional[int] = None


class ToolCall(BaseModel):
    name: str
    arguments: Dict[str, Any]

class LLMResponse(BaseModel):
    content: str
    model: Optional[str] = None
    provider: Optional[str] = None

    chunk_state: str = None # continue or last
    id: Optional[str] = None

    usage: Optional[TokenUsage] = None

    tool_calls: Optional[List[ToolCall]] = None

    raw: Optional[Dict[str, Any]] = None