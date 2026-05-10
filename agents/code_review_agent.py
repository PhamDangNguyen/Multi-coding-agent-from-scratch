from typing import Any, Dict, Optional

from .base import BaseAgent


class CodeReviewAgent(BaseAgent[str, Dict[str, Any]]):
	"""Agent for reviewing code."""

	agent_name =  "CodeReviewAgent"
	agent_description = "Reviews code to detect bugs, anti-patterns, security risks, style inconsistencies, and maintainability issues such as missing exception handling, duplicate logic, or oversized functions."

	async def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		# For safety, we don't execute commands here; just echo intent.
		
		return {"result": f"Would run bash command: {task}"}

	async def update_system_prompt(self, update_prompt: Optional[str] = None) -> str:
		pass

	async def build_sys_prompt(self, system_prompt: Optional[str] = None) -> str:
		return system_prompt or "You are a code review assistant. Analyze code for potential issues, best practices, and improvements."
