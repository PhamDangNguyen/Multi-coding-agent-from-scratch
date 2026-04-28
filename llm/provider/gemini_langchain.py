from typing import Optional
from ..base import BaseLLMClient, BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from schemas.llm.llm_response import LLMResponse, TokenUsage, ToolCall

class GeminiClientLangChain(BaseLLMClient):
    """Google Gemini LLM Client using by LangChain"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash", temperature: float = 0.7, max_tokens: Optional[int] = None, max_retries: int = 2):
        super().__init__(api_key, model, temperature, max_tokens)
        self.client = ChatGoogleGenerativeAI(api_key=self.api_key, model=self.model, temperature=self.temperature, max_tokens=self.max_tokens, max_retries=max_retries)

    def _convert_messages(self, messages: list[BaseMessage]):
        message_normalized = []

        for msg in messages:
            if msg.role == "system":
                message_normalized.append(("system", msg.content))
            else:
                message_normalized.append(("human", msg.content))
        return message_normalized
    
    def build_response(self, msg) -> LLMResponse:
        usage_meta = getattr(msg, "usage_metadata", {}) or {}
        response_metadata= getattr(msg, "response_metadata", {}) or {}
        return LLMResponse(
            content=msg.content,
            model=response_metadata.get("model_name"),
            provider=response_metadata.get("model_provider"),
            chunk_state= "last" if (response_metadata.get("finish_reason")=="stop" or getattr(msg, "chunk_position")=="last") else "continue",
            id=getattr(msg, "id", None),

            usage=TokenUsage(
                input_tokens=usage_meta.get("input_tokens"),
                output_tokens=usage_meta.get("output_tokens"),
                total_tokens=usage_meta.get("total_tokens"),
                reasoning_tokens=usage_meta.get("output_token_details", {}).get("reasoning"),
            ),

            tool_calls=[
                ToolCall(name=tc["name"], arguments=tc["args"])
                for tc in getattr(msg, "tool_calls", [])
            ] if getattr(msg, "tool_calls", None) else None,

            raw={
                "response_metadata": msg,
                "additional_kwargs": getattr(msg, "additional_kwargs", None)
            }
        )
    
    async def generate(
        self,
        messages: list[BaseMessage],
    ) -> str:
        """Generate text response from Gemini"""
        message_normalized = self._convert_messages(messages)
        response =  self.client.invoke(message_normalized)
        return self.build_response(response)
    
    async def stream_generate(
        self,
        messages: list[BaseMessage]
    ):
        message_normalized = self._convert_messages(messages)

        async for chunk in self.client.astream(message_normalized):
            if chunk:
                yield self.build_response(chunk)