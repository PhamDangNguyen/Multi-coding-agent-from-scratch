import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]  
sys.path.append(str(ROOT))
from typing import List
from schemas.llm.llm_message import BaseMessage
from llm import OpenAIClientLangChain
from agents.base import BaseAgent
from agents import Agent_farm
from prompts import load_prompt
from dotenv import load_dotenv
from schemas.agents.planner_response import PlannerResponse
load_dotenv()

from log_set import AppLogger
logger = AppLogger(__name__)

class AgentPlanner(BaseAgent[str, PlannerResponse]):
    """Agent planner that takes a user task and returns a list of tasks with assigned agents"""
    def __init__(self, llm: OpenAIClientLangChain):
        self.llm = llm
        self.system_prompt_base = load_prompt("llm_systems/planner.md")
        self.message_history: List[BaseMessage] = []  
        self.message_history.append(self.build_sys_prompt())

    def build_sys_prompt(self) -> str:
        system_message=BaseMessage(
            role="system",
            content=self.system_prompt_base + "\n\nAvailable agents:\n" + str(Agent_farm) + "\n Return ONLY JSON list: [{\"task\": \"...\", \"agent\": \"...\"}]"
        )
        return system_message
       
    async def run(self, task: str) -> PlannerResponse:
        prompt = f"""
            User want to do this task:
            {task}
            Break down the task into smaller tasks and assign each task to the most suitable agent from the available agents list.
        """

        self.message_history.append(BaseMessage(role="user", content=prompt))
    
        res = await self.llm.generate(self.message_history)
        if res is not None:
            logger.log("INFO", f"Planner LLM generated susscessfully!!")

        return PlannerResponse(Response=json.loads(res.content))

    
if __name__ == "__main__":
    import asyncio
    import os
    from rich import print
    api_key = os.getenv("OPENAI_API")
    model = os.getenv("OPENAI_MODEL")
    planner = AgentPlanner(OpenAIClientLangChain(api_key=api_key, model=model))
    res = asyncio.run(planner.run("I want to build a website that sells handmade crafts simplify."))
    print(res)