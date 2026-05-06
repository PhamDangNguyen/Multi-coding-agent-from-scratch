from typing import Any, Dict, Optional

from .base import BaseAgent


class BashAgent(BaseAgent[str, Dict[str, Any]]):
	"""Example bash/terminal agent."""

	agent_name =  "BashAgent"
	agent_description = "Using bash commands safely."

	async def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		# For safety, we don't execute commands here; just echo intent.
		return {"result": f"Would run bash command: {task}"}

	async def build_sys_prompt(self, system_prompt: Optional[str] = None) -> str:
		return system_prompt or "You are a shell helper. Explain command usage and safety considerations."
