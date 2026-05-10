import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]  
sys.path.append(str(ROOT))
from typing import List, Optional
from schemas.llm.llm_message import BaseMessage
from llm import OpenAIClientLangChain, GeminiClientLangChain
from agents.base import BaseAgent
from agents import Agent_farm
from skill import Skill_loader
from prompts import load_prompt
from dotenv import load_dotenv
from schemas.agents.planner_response import PlannerResponse
load_dotenv()

from log_set import AppLogger
logger = AppLogger(__name__)

class AgentPlanner(BaseAgent[str, PlannerResponse]):
    """Agent planner that takes a user task and returns a list of tasks with assigned agents"""
    def __init__(self, llm: OpenAIClientLangChain|GeminiClientLangChain):
        self.llm = llm
        self.system_prompt_base = load_prompt("llm_systems/planner.md")
        self.message_history: List[BaseMessage] = []  
        self.message_history.append(self.build_sys_prompt())

    def build_sys_prompt(self) -> BaseMessage:
        content = f"""
        {self.system_prompt_base}

        Available agents:
        {Agent_farm}

        Available skills to analyze for each task:
        {Skill_loader}

        Instructions:
        - Break the request into atomic executable tasks
        - Assign the most suitable agent
        - Infer recommended skills for each task
        - Define dependency order when needed
        - If both ProjectArchitectAgent and CodingAgent are present, always create the planning/architecture task(s) assigned to ProjectArchitectAgent first. Ensure any CodingAgent task has a `depends_on` referencing the corresponding ProjectArchitectAgent task(s).
        - Sort the output array by execution order (dependencies first). Place ProjectArchitectAgent tasks before CodingAgent tasks when applicable.
        - Return ONLY valid JSON

        Output format:
        [{{
            "id": "...",
            "agent": "......",
            "task": "......",
            "depends_on": ["...", "...", ...],
            "recommended_skills": ["...", "...", ...]
        }}]
        """

        return BaseMessage(
            role="system",
            content=content.strip()
        )
    
    def update_system_prompt(self, update_prompt: Optional[str] = None) -> None:
            if not update_prompt:
                return
            self.message_history[0].content = self.message_history[0].content + "\n\n" + update_prompt 
       
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
    res = asyncio.run(planner.run("create file a.txt this is summary file from b.txt file"))
    print(res)