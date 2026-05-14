from typing import Generic, TypeVar, Optional, Dict, Any
from schemas.llm.llm_message import BaseMessage
import tiktoken
from dotenv import load_dotenv
import os
load_dotenv()

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class BaseAgent(Generic[InputT, OutputT]):
    """Minimal BaseAgent contract for agents in the `agents` package.

    - `agent_name` is used as the registry key when subscribing.
    - `subscribe` by default registers the instance into a provided
      registry mapping.
    """

    agent_name: Optional[str] = None
    agent_description: Optional[str] = None

    async def run(self, task: InputT, tools: Optional[Dict[str, Any]] = None) -> OutputT:
        raise NotImplementedError()

    async def build_sys_prompt(self, system_prompt: Optional[str] = None) -> str:
        raise NotImplementedError()
    
    async def update_system_prompt(self, update_prompt: Optional[str] = None) -> str:
        raise NotImplementedError()    

    def reset_message_history(self, keep_system: bool = True):
        if not keep_system:
            self.message_history = []
            return

        self.message_history = [
            message
            for message in self.message_history
            if getattr(message, "role", None) == "system"
        ]

    async def compress_message_history(self, max_tokens: int = 200000):
        total_content = ""
        system_mess = None
        last_message = self.message_history[-1] if self.message_history else None
        for message in self.message_history:
            if getattr(message, "role", None) == "system":
                system_mess = message
            else: 
                total_content += getattr(message, "content", "") + "\n"
                
        encoding = tiktoken.get_encoding("o200k_base")
        conten_tokens = encoding.encode(str(total_content))
        last_message_tokens = encoding.encode(str(last_message.content))
        if len(conten_tokens) > max_tokens:
            if len(conten_tokens) > 250000:
                total_content = total_content[-200000:]
            if len(last_message_tokens) > 50000:
                last_message.content = last_message.content[0:50000]
            prompt_compress = [
                BaseMessage(
                    role="system",
                    content=f"""You are a helpful assistant that compresses the message history for a multi-agent coding system. Your task is to summarize the message history into a concise format that preserves important information while reducing token count."""),
                BaseMessage(
                    role="user",
                    content=f"""Here is the message history that needs to be compressed:
                    {total_content}
                    Return only the compressed summary 5000 words without any additional commentary."""
                ),
                last_message
            ]
            res = await self.llm.generate(prompt_compress)
            summary = getattr(res, "content", str(res))
            self.message_history = [
                message
                for message in [system_mess, BaseMessage(role="user", content=summary), last_message]
                if message is not None
            ]
            

    def subscribe(self, registry: Dict[str, "BaseAgent"]):
        """Register this agent instance into `registry`.

        Default behaviour: use `agent_name` or class name lowercased.
        """
        name = self.agent_name
        des = self.agent_description
        registry[name] = des
