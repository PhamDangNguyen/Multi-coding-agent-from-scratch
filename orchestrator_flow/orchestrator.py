"""
React Multi-Agent Orchestrator – LangGraph

Architecture:

query
  ↓
planner
  ↓
executor
  ↓
END

planner:
- split query into structured tasks

executor:
- dispatch task to ReactAgent runtime

react agent:
- think
- choose tool
- execute tool
- observe
- repeat
- final answer
"""

import os
import sys
import asyncio

from pathlib import Path
from rich import print
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END

sys.path.append(str(Path(__file__).resolve().parents[1]))

from orchestrator_flow.planner import AgentPlanner
from agents import Agent_farm
from tools import TOOLS_DICT
from schemas.orchestrator.state_graph import (Task,State)
from llm.provider.openai_langchain import OpenAIClientLangChain
from orchestrator_flow.react_agent_runtime import ReactAgentRuntime

load_dotenv()
LLM = OpenAIClientLangChain(api_key=os.getenv("OPENAI_API"), model=os.getenv("OPENAI_MODEL"))

# Agent declareation
PLANNER = AgentPlanner(LLM)

# Planner Node
async def planner_node(state: State):

    print("\n[Planner] Creating plan...")

    res = await PLANNER.run(state["query"])

    raw_plan = res.Response

    tasks = []

    for idx, step in enumerate(raw_plan):

        task = Task(
            id=f"task_{idx + 1}",
            task=step["task"],
            agent=step["agent"],
            status="pending",
            result=None,
            error=None,
        )

        tasks.append(task)

    print(f"[Planner] Total Tasks: {len(tasks)}")

    return {
        **state,
        "tasks": tasks,
    }

# ─────────────────────────────────────────────────────────────
# Executor Node
# ─────────────────────────────────────────────────────────────

async def executor_node(state: State):

    tasks = state["tasks"]

    shared_memory = state["shared_memory"]

    for task in tasks:

        task["status"] = "running"

        task_id = task["id"]
        task_text = task["task"]
        agent_name = task["agent"]

        print("\n" + "=" * 80)
        print(f"[Executor] {task_id}")
        print(f"Task  : {task_text}")
        print(f"Agent : {agent_name}")

        # ─────────────────────────────────────────────
        # Get Agent
        # ─────────────────────────────────────────────

        agent = Agent_farm.get(agent_name)

        if not agent:

            task["status"] = "failed"
            task["error"] = f"Agent not found: {agent_name}"

            continue

        # ─────────────────────────────────────────────
        # React Runtime
        # ─────────────────────────────────────────────

        runtime = ReactAgentRuntime(
            agent=agent,
            tools=TOOLS_DICT,
        )

        result = await runtime.run(
            task=task_text,
            shared_memory=shared_memory,
        )

        task["status"] = result["status"]
        task["result"] = result["result"]

        print(f"\n[Done] {task_id}")

    # ─────────────────────────────────────────────────
    # Final Answer
    # ─────────────────────────────────────────────────

    outputs = []

    for task in tasks:

        outputs.append(
            f"""
[{task['id']}]

Task:
{task['task']}

Agent:
{task['agent']}

Status:
{task['status']}

Result:
{task['result']}
            """.strip()
        )

    final_answer = "\n\n".join(outputs)

    return {
        **state,
        "tasks": tasks,
        "final_answer": final_answer,
    }

# ─────────────────────────────────────────────────────────────
# Build Graph
# ─────────────────────────────────────────────────────────────

def build_graph():

    graph = StateGraph(State)

    graph.add_node("planner", planner_node)

    graph.add_node("executor", executor_node)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "executor")

    graph.add_edge("executor", END)

    return graph.compile()

# ─────────────────────────────────────────────────────────────
# Singleton App
# ─────────────────────────────────────────────────────────────

APP = build_graph()

# ─────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────

async def run(query: str):

    initial_state = {
        "query": query,

        "tasks": [],

        "shared_memory": {},

        "final_answer": "",
    }

    result = await APP.ainvoke(initial_state)

    return result

# ─────────────────────────────────────────────────────────────
# Test
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":

    query = """
Read README.md
understand project
then create hello.py
with simple hello world
"""

    result = asyncio.run(run(query))

    print("\n" + "=" * 80)
    print("FINAL RESULT")
    print("=" * 80)

    print(result["final_answer"])