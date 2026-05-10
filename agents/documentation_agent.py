from typing import Any, Dict, Optional

from .base import BaseAgent


class DocumentationAgent(BaseAgent[str, Dict[str, Any]]):
	"""Agent for generating documentation."""

	agent_name = "DocumentationAgent"
	agent_description = "Generates project documentation, including README files, API docs, and user guides, ensuring clarity and completeness for developers and end-users."

	async def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		# Minimal example: echo back the task as 'result'
		return {"result": f"Handled documentation task: {task}"}
	async def update_system_prompt(self, update_prompt: Optional[str] = None) -> str:
		pass
	async def build_sys_prompt(self, system_prompt: Optional[str] = None) -> str:
		return system_prompt or "You are a documentation assistant. Provide clear and comprehensive documentation guidance."
