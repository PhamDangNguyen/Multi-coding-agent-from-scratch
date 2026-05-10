from typing import Any, Dict, Optional

from .base import BaseAgent


class TestAgent(BaseAgent[str, Dict[str, Any]]):
	"""Agent for generating tests."""

	agent_name =  "TestAgent"
	agent_description = "Generates unit, integration, and API tests, including mock data and automated test suites using tools like pytest, Playwright, and Postman."

	async def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		# For safety, we don't execute commands here; just echo intent.
		return {"result": f"Would run bash command: {task}"}
	async def update_system_prompt(self, update_prompt: Optional[str] = None) -> str:
		pass
	async def build_sys_prompt(self, system_prompt: Optional[str] = None) -> str:
		return system_prompt or "You are a test generation assistant. Create tests for various scenarios, including edge cases and error handling."
