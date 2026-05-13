"""Production-oriented LangGraph orchestrator for the multi-agent flow.

Flow:
    user query -> planner -> dependency-aware executor -> final answer

The orchestrator keeps the public `run(query)` API stable while adding:
- lazy app/LLM initialization
- planner output validation
- dependency-aware task execution
- per-task agent isolation
- runtime timeout/error handling
- shared memory updates between tasks
"""

from __future__ import annotations

import asyncio
import os
import sys
from collections.abc import Awaitable, Mapping, Sequence
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langgraph.graph import END, StateGraph

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from log_set import AppLogger
from schemas.orchestrator.state_graph import State, Task
from schemas.orchestrator.config import OrchestratorConfig
from agents import load_default_agent_instances, AgentClass, build_llm
from orchestrator_flow.react_agent_runtime import ReactAgentRuntime
from tools import TOOLS_DICT, TOOLS_INSTANCE
from rich import print

load_dotenv()

logger = AppLogger(__name__)

class MultiAgentOrchestrator:
    def __init__(
        self,
        config: OrchestratorConfig | None = None,
        agent_classes: Mapping[str, AgentClass] | None = None,
    ):
        self.config = config
        self._agent_classes = dict(agent_classes)
        self._llm_client = build_llm(config)

    async def planner_node(self, state: State) -> State:
        query = state.get("query")
        shared_memory = dict(state.get("shared_memory"))

        if not query:
            raise ValueError("Query is empty")

        planner = self._agent_classes.get("AgentPlanner")

        response = await self._with_timeout(
            planner.run(query),
            self.config.planner_timeout_seconds,
        )
        print("Raw planner response:", response)
        raw_plan = getattr(response, "Response", response)
        tasks = self._normalize_tasks(raw_plan)

        logger.info(f"Planner created {len(tasks)} task(s)")

        return {
            **state,
            "tasks": tasks,
            "shared_memory": shared_memory,
            "final_answer": "",
        }

    async def executor_node(self, state: State) -> State:
        tasks = list(state.get("tasks"))
        shared_memory = dict(state.get("shared_memory"))

        while True:
            pending = [task for task in tasks if task.get("status") == "pending"]
            if not pending:
                break

            progress = False
            task_by_id = {task["id"]: task for task in tasks}

            for task in pending:
                blocked_by = self._failed_dependencies(task, task_by_id)
                if blocked_by:
                    task["status"] = "failed"
                    task["error"] = "Skipped because dependency failed: " + ", ".join(blocked_by)
                    self._remember_task(shared_memory, task)
                    progress = True
                    continue

                if not self._dependencies_completed(task, task_by_id):
                    continue

                progress = True
                await self._execute_task(task, shared_memory)

                if self.config.stop_on_failure and task.get("status") == "failed":
                    self._fail_pending_tasks(tasks, "Stopped because a previous task failed")
                    break

            if self.config.stop_on_failure and any(task.get("status") == "failed" for task in tasks):
                break

            if not progress:
                self._fail_pending_tasks(tasks, "Dependency cycle or unresolved dependency")
                break

        final_answer = self._format_final_answer(tasks)
        return {
            **state,
            "tasks": tasks,
            "shared_memory": shared_memory,
            "final_answer": final_answer,
        }

    async def _execute_task(self, task: Task, shared_memory: dict[str, Any]) -> None:
        task_id = task["id"]
        agent_name = task["agent"]
        task_text = task["task"]

        logger.info(f"Executing {task_id} with {agent_name}")
        task["status"] = "running"

        agent = self._agent_classes.get(agent_name)
        agent.reset_message_history(keep_system=True)
        runtime = ReactAgentRuntime(agent=agent, tools_des=TOOLS_DICT, tools_instance=TOOLS_INSTANCE, max_iterations=self.config.max_iterations)
        result = await self._with_timeout(runtime.run(task=task_text, shared_memory=shared_memory), self.config.task_timeout_seconds)
        runtime_status = result.get("status")

        if runtime_status == "completed":
            task["status"] = "completed"
            task["result"] = result.get("result")
            task["error"] = None
        else:
            task["status"] = "failed"
            task["result"] = result.get("result")
            task["error"] = result.get("error") or f"Runtime status: {runtime_status}"
        
        task["summary"] = await self._summarize_task_result(task)
        self._remember_task(shared_memory, task)

    def _normalize_tasks(self, raw_plan: Any) -> list[Task]:
        if raw_plan is None:
            raise ValueError("Planner returned no plan")
        tasks: list[Task] = []
        for _, item in enumerate(raw_plan, start=1):
            task_id, task_text, agent_name, depends_on, recommended_skills = item.id, item.task, item.agent, item.depends_on, item.recommended_skills
            task: Task = {
                "id": task_id,
                "task": task_text,
                "agent": agent_name,
                "depends_on": depends_on,
                "skill": recommended_skills,
                "status": "pending",
                "result": None,
                "error": None,
            }

            tasks.append(task)
        return tasks

    def _failed_dependencies(self, task: Task, task_by_id: Mapping[str, Task],) -> list[str]:
        failed: list[str] = []
        for dep in task.get("depends_on"):
            dep_task = task_by_id.get(dep)
            if dep_task and dep_task.get("status") == "failed":
                failed.append(dep)
        return failed

    def _dependencies_completed(self, task: Task, task_by_id: Mapping[str, Task]) -> bool:
        for dep in task.get("depends_on"):
            dep_task = task_by_id.get(dep)
            if not dep_task or dep_task.get("status") != "completed":
                return False
        return True

    def _remember_task(self, shared_memory: dict[str, Any], task: Task) -> None:
        shared_memory[task["id"]] = {"agent": task.get("agent"), "task": task.get("task"), "status": task.get("status"), "summary": task.get("summary"), "error": task.get("error")}
        shared_memory["last_task_id"] = task["id"]

    def _fail_pending_tasks(self, tasks: list[Task], reason: str) -> None:
        for task in tasks:
            if task.get("status") == "pending":
                task["status"] = "failed"
                task["error"] = reason

    def _format_final_answer(self, tasks: Sequence[Task]) -> str:
        sections: list[str] = []
        for task in tasks:
            status = task.get("status")
            result = task.get("result")
            error = task.get("error")

            body = result if status == "completed" else error
            sections.append(
                "\n".join(
                    [
                        f"[{task.get('id')}]",
                        f"Agent: {task.get('agent')}",
                        f"Status: {status}",
                        f"Task: {task.get('task')}",
                        f"Result: {body}",
                    ]
                )
            )
        return "\n\n".join(sections)

    async def _with_timeout(self, awaitable: Awaitable[Any], timeout_seconds: float | None) -> Any:
        if timeout_seconds is None:
            return await awaitable
        return await asyncio.wait_for(awaitable, timeout=timeout_seconds)

    async def _summarize_task_result(self, task: Task) -> str:
        agent_name = task.get("agent")
        task_text = task.get("task")
        status = task.get("status")
        result = task.get("result")
        error = task.get("error")
        if status != "completed":
            return f"Task failed.\n Agent: {agent_name}\n Error: {error}\n Result: {result}"
        summarizer = self._agent_classes.get("AgentPlanner")
        if summarizer is None:
            return self._truncate(result, 4000)
        prompt = f"""
        You are a memory summarizer for a multi-agent coding system.
        Summarize the completed task result into a concise handoff memory for downstream agents.
        Focus only on actionable facts. Remove verbose logs, repeated tool outputs, and long explanations.
        Return this structure:
        ## What was done
        - ...
        ## Files/folders created or modified
        - path — purpose
        ## Important decisions
        - ...
        ## Instructions for next agents
        - ...
        ## Risks / notes
        - ...
        Agent: {agent_name}
        Task:
        {task_text}
        Raw task result:
        {result}
        """
        response = await self._with_timeout(summarizer.run(prompt),self.config.planner_timeout_seconds)
        return getattr(response, "content", response)



def build_graph(orchestrator: MultiAgentOrchestrator | None = None):
    orchestrator = orchestrator

    graph = StateGraph(State)
    graph.add_node("planner", orchestrator.planner_node)
    graph.add_node("executor", orchestrator.executor_node)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "executor")
    graph.add_edge("executor", END)
    return graph.compile()

async def run(query: str, *, orchestrator: MultiAgentOrchestrator | None = None, shared_memory: Mapping[str, Any] | None = None) -> State:
    if not query or not query.strip():
        raise ValueError("query must not be empty")

    initial_state: State = {
        "query": query.strip(),
        "tasks": [],
        "shared_memory": dict(shared_memory or {}),
        "final_answer": "",
    }

    graph = build_graph(orchestrator)
    return await graph.ainvoke(initial_state)


if __name__ == "__main__":
    from rich import print

    llm_client = build_llm(OrchestratorConfig())
    orchestrator= MultiAgentOrchestrator(config=OrchestratorConfig(), agent_classes=load_default_agent_instances(llm_client))
    query = "Trong folder '/home/dangnguyen/Side_project/Multi-agent-from-scratch/code_test', hãy code một API tính cộng 2 số bằng python theo pattern design."

    output = asyncio.run(run(query, orchestrator=orchestrator))
    print(output["final_answer"])
