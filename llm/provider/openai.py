from typing import Optional
import json 
from openai import AsyncOpenAI
from ..base import BaseLLMClient, BaseMessage
from schemas.llm.llm_response import LLMResponse, TokenUsage, ToolCall

class OpenAIClient(BaseLLMClient):
    """OpenAI LLM Client"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini", temperature: float = 0.7, max_tokens: Optional[int] = None):
        super().__init__(api_key, model, temperature, max_tokens)
        self.client = AsyncOpenAI(api_key=api_key)
    
    def build_response(self, resp) -> LLMResponse:
        choice = resp.choices[0]

        is_stream = hasattr(choice, "delta")

        msg = choice.delta if is_stream else choice.message

        content = getattr(msg, "content", None) or ""

        tool_calls = []
        tc_list = getattr(msg, "tool_calls", None)

        if tc_list:
            for tc in tc_list:
                args = tc.function.arguments
                if not isinstance(args, dict):
                    try:
                        args = json.loads(args)
                    except:
                        args = {}

                tool_calls.append(
                    ToolCall(
                        name=tc.function.name,
                        arguments=args,
                    )
                )

        tool_calls = tool_calls or None

        finish_reason = choice.finish_reason
        chunk_state = "last" if finish_reason is not None else "continue"

        usage = None
        if getattr(resp, "usage", None):
            u = resp.usage
            usage = TokenUsage(
                input_tokens=u.prompt_tokens,
                output_tokens=u.completion_tokens,
                total_tokens=u.total_tokens,
                reasoning_tokens=(
                    u.completion_tokens_details.reasoning_tokens
                    if getattr(u, "completion_tokens_details", None)
                    else None
                ),
            )
        return LLMResponse(
            content=content,
            model=resp.model,
            provider="openai",
            id=resp.id,
            chunk_state=chunk_state,
            usage=usage,
            tool_calls=tool_calls,
            raw=resp.model_dump(),
        )
    async def generate(
        self,
        messages: list[BaseMessage]
    ) -> LLMResponse:
        """Generate text response từ OpenAI"""
        formatted_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=formatted_messages,
            temperature=self.temperature,
            max_completion_tokens=self.max_tokens
        )
        
        return self.build_response(response)
    
    async def stream_generate(
        self,
        messages: list[BaseMessage]
    ):
        """Stream text response từ OpenAI"""
        formatted_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        async with await self.client.chat.completions.create(
            model=self.model,
            messages=formatted_messages,
            temperature=self.temperature,
            max_completion_tokens=self.max_tokens,
            stream=True,
        ) as stream:
            async for chunk in stream:
                if chunk:
                    yield self.build_response(chunk)
