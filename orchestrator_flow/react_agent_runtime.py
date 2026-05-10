import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from tools import TOOLS_INSTANCE, TOOLS_DICT
from schemas.tools.bash import BASH_TOOLS_SCHEMA
from agents.project_architect_agent import ProjectArchitectAgent
from llm import OpenAIClientLangChain
from schemas.llm.llm_message import BaseMessage
from log_set import AppLogger

logger = AppLogger(__name__)

class ReactAgentRuntime:
    def __init__(self, agent, tools_des, tools_instance, max_iterations: int = 5):
        self.agent = agent
        self.tools_des = tools_des
        self.tools_instance = tools_instance
        self.max_iterations = max_iterations
        self.schema_map = {tool["name"]: tool for tool in BASH_TOOLS_SCHEMA}

    def tools_prompt(self, tools: list[str] | None = None):
        target = tools or list(self.tools_des.keys())
        return "\n".join(f"- {name}: {self.tools_des[name]}" for name in target if name in self.tools_des)

    def get_tool_schema(self, selected_tools: list[str]) -> list[dict]:
        return [self.schema_map[name] for name in selected_tools if name in self.schema_map]
    
    def safe_parse(self, text: str):
        start, end = text.find("{"), text.rfind("}")
        if start == -1 or end == -1:
            raise ValueError(f"Invalid JSON output:\n{text}")
        return json.loads(text[start:end + 1])

    async def plan_tools(self,task: str) -> list[str]:
        prompt = f"""
            You are a tool planner.
            TASK:
            {task}
            AVAILABLE TOOLS:
            {self.tools_prompt()}
            Return ONLY JSON:
            {{
            "tools": ["tool1", "tool2"]
            }}
        """
        response = await self.agent.run(prompt)
        parsed = self.safe_parse(response.content)
        return parsed.get("tools")

    async def run(self,task: str,shared_memory: dict):
        selected_tools = await self.plan_tools(task)
        logger.log("INFO",f" Agent {self.agent.agent_name} selected tools: {selected_tools}")
        tools_schema = self.get_tool_schema(selected_tools)
        prompt_user = f"""
            You are a helpful AI agent.
            AVAILABLE TOOLS:
            {self.tools_prompt(selected_tools)}
            Rules:
            - Use tools only when necessary
            - After task is completed, return final answer
            - Do not call the same tool repeatedly
            - If observation indicates success, stop calling tools
        """
        scratchpad = []
        for step in range(self.max_iterations):
            logger.log("INFO",f"Agent {self.agent.agent_name} running step {step + 1}")
            response = await self.agent.run(task=prompt_user,tools=tools_schema)
            # save assistant response
            if response.content:
                self.agent.message_history.append(BaseMessage(role="assistant",content=response.content))
            if not response.tool_calls:
                logger.log("INFO","Task completed")
                self.agent.message_history.append(BaseMessage(role="system",content=f"Task completed: {response.content}"))
                return {"status": "completed","result": response.content,"scratchpad": scratchpad}
            for tool_call in response.tool_calls:
                tool_name = tool_call.name
                tool_args = tool_call.arguments
                logger.log("INFO",f"Calling tool: {tool_name}")
                tool = self.tools_instance.get(tool_name)
                if not tool:
                    observation = (f"Tool not found: {tool_name}")
                else:
                    try:
                        observation = await tool.execute(**tool_args)
                    except Exception as e:
                        observation = (f"Tool execution error: {e}")

                scratchpad.append({
                    "tool": tool_name,
                    "args": tool_args,
                    "observation": observation,
                })
                self.agent.message_history.append(BaseMessage(role="tool",content=str(observation) + f"\n name={tool_name}"))
        
        return {
            "status": "max_iterations",
            "result": "Stopped due to max iterations",
            "scratchpad": scratchpad,
        }

# if __name__ == "__main__":
#     import asyncio
#     import os
#     from rich import print
#     api_key = os.getenv("OPENAI_API")
#     model = os.getenv("OPENAI_MODEL")
#     agent = ProjectArchitectAgent(OpenAIClientLangChain(api_key=api_key,model=model))
#     runtime = ReactAgentRuntime(agent=agent,tools_des=TOOLS_DICT,tools_instance=TOOLS_INSTANCE,max_iterations=5)
#     result = asyncio.run(
#         runtime.run(
#             task=(
#                 "Đọc repo '/home/dangnguyen/Side_project/Multi-agent-from-scratch' và tóm tắt vào file a.txt 5 dòng xem repo làm gì"),shared_memory={}))
#     print(result)