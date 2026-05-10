from typing import Any, Dict, Optional

from .base import BaseAgent


class CodingAgent(BaseAgent[str, Dict[str, Any]]):
	"""Example coding agent."""

	agent_name = "CodingAgent"
	agent_description = "coding, execute shell/file operations, edit/write source code, run commands, manipulate files, etc."

	async def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		# Minimal example: echo back the task as 'result'
		return {"result": f"Handled coding task: {task}"}
	async def update_system_prompt(self, update_prompt: Optional[str] = None) -> str:
		pass
	async def build_sys_prompt(self, system_prompt: Optional[str] = None) -> str:
		return system_prompt or "You are a coding assistant. Provide concise code-focused replies."
