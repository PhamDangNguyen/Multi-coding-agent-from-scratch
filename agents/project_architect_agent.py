from typing import Any, Dict, Optional, List
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]  
sys.path.append(str(ROOT))
from agents.base import BaseAgent
from schemas.llm.llm_message import BaseMessage
from llm import OpenAIClientLangChain, GeminiClientLangChain
from prompts import load_prompt
from dotenv import load_dotenv
load_dotenv()
from schemas.tools.bash import BASH_TOOLS_SCHEMA
from log_set import AppLogger
logger = AppLogger(__name__)
class ProjectArchitectAgent(BaseAgent[str, Dict[str, Any]]):
	"""Agent for defining project architecture."""

	agent_name =  "ProjectArchitectAgent"
	agent_description = """
		Can read file, repo , and system information to design project architecture, including:
		- Defining module structure and organization
		- Identifying key components and their interactions
		- Recommending design patterns and best practices
		- Providing high-level implementation guidance
	"""
	def __init__(self, llm: OpenAIClientLangChain|GeminiClientLangChain):
		self.llm = llm
		self.system_prompt_base = load_prompt("llm_systems/project_architect.md")
		self.message_history: List[BaseMessage] = []  
		self.message_history.append(self.build_sys_prompt())

	async def run(self, task: str, tools: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		prompt = f"""User want to do this task: {task}"""
		self.message_history.append(BaseMessage(role="user", content=prompt))
		res = await self.llm.generate(self.message_history, tools=tools)
		if res is not None:
			logger.log("INFO",f"ProjectArchitectAgent generate sussessfully !!")
		return res 
	
	def update_system_prompt(self, update_prompt: Optional[str] = None) -> None:
		if not update_prompt:
			return
		self.message_history[0].content = self.message_history[0].content + "\n\n" + update_prompt 

	def build_sys_prompt(self) -> BaseMessage:
		content = self.system_prompt_base
		return BaseMessage(
			role="system",
			content=content.strip()
		)
	
if __name__ == "__main__":
	import asyncio
	import os
	from rich import print
	api_key = os.getenv("OPENAI_API")
	model = os.getenv("OPENAI_MODEL")
	project_architect = ProjectArchitectAgent(OpenAIClientLangChain(api_key=api_key, model=model))
	res = asyncio.run(project_architect.run("read .txt file from llm dir", tools=BASH_TOOLS_SCHEMA))
	print(res)