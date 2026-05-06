from typing import Any, Dict, Optional

from .base import BaseAgent


class CodingAgent(BaseAgent[str, Dict[str, Any]]):
	"""Example coding agent."""

	agent_name = "CodingAgent"
	agent_description = "Handling coding-related tasks."

	async def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		# Minimal example: echo back the task as 'result'
		return {"result": f"Handled coding task: {task}"}

	async def build_sys_prompt(self, system_prompt: Optional[str] = None) -> str:
		return system_prompt or "You are a coding assistant. Provide concise code-focused replies."
