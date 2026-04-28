from typing import Optional
import google.genai as genai
from ..base import BaseLLMClient, BaseMessage
from google.genai.types import GenerateContentConfig
from schemas.llm.llm_response import LLMResponse, TokenUsage, ToolCall

class GeminiClient(BaseLLMClient):
    """Google Gemini LLM Client"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash", temperature: float = 0.7, max_tokens: Optional[int] = None):
        super().__init__(api_key, model, temperature, max_tokens)
        self.client = genai.Client(api_key=self.api_key)

    def _convert_messages(self, messages: list[BaseMessage]):  
        system_instruction = []
        contents = []

        for msg in messages:
            if msg.role == "system":
                system_instruction.append(msg.content)
            else:
                contents.append({
                    "role": msg.role,
                    "parts": [{"text": msg.content}]
                })
        return contents, system_instruction
    
    def build_response(self, resp) -> LLMResponse:
        tool_calls = []
        for cand in resp.candidates:
            for part in cand.content.parts:

                if part.function_call:
                    tool_calls.append(
                        ToolCall(
                            name=part.function_call["name"],
                            arguments=part.function_call.get("args", {}),
                        )
                    )

                if part.tool_call:
                    tool_calls.append(
                        ToolCall(
                            name=part.tool_call["name"],
                            arguments=part.tool_call.get("args", {}),
                        )
                    )
        candidates = getattr(resp, "candidates", None)
        if not candidates:
            chunk_state  = "continue"
        else:
            finish_reason = candidates[0].finish_reason
            if finish_reason is not None:
                chunk_state = "last"
            else:
                chunk_state = "continue"
        return LLMResponse(
            content=resp.candidates[0].content.parts[0].text,
            model=resp.model_version,
            provider="gemini",
            id=resp.response_id,
            chunk_state=chunk_state,
            usage=TokenUsage(
                input_tokens=resp.usage_metadata.prompt_token_count,
                output_tokens=resp.usage_metadata.candidates_token_count,
                total_tokens=resp.usage_metadata.total_token_count,
                reasoning_tokens=resp.usage_metadata.thoughts_token_count,
            ),
            tool_calls = tool_calls if tool_calls else None,
            raw=resp.model_dump(),
        )
    
    async def generate(
        self,
        messages: list[BaseMessage]
    ) -> str:
        """Generate text response from Gemini"""
        formatted_messages, system_instruction = self._convert_messages(messages)
        
        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=formatted_messages,
            config=GenerateContentConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
                system_instruction=system_instruction,
            ),
        )
        
        return self.build_response(response)
    
    async def stream_generate(
        self,
        messages: list[BaseMessage],
    ):
        """Stream text response from Gemini"""
        formatted_messages, system_instruction = self._convert_messages(messages)

        stream = await self.client.aio.models.generate_content_stream(
            model=self.model,
            contents=formatted_messages,
            config=GenerateContentConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
                system_instruction=system_instruction,
            ),
        )

        async for chunk in stream:
            if chunk:
                yield self.build_response(chunk)