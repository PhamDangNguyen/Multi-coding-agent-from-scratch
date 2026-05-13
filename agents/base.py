from typing import Generic, TypeVar, Optional, Dict, Any

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

    def subscribe(self, registry: Dict[str, "BaseAgent"]):
        """Register this agent instance into `registry`.

        Default behaviour: use `agent_name` or class name lowercased.
        """
        name = self.agent_name
        des = self.agent_description
        registry[name] = des
