from typing import Literal, TypedDict, Any

TaskStatus = Literal[
    "pending",
    "running",
    "completed",
    "failed",
]

class Task(TypedDict, total=False):
    id: str

    task: str

    agent: str

    depends_on: list[str] | None

    status: TaskStatus

    tool_name: str | None
    
    skill: list[str] | None

    tool_args: dict[str, Any] | None

    tool_result: str | None

    result: str | None

    error: str | None


class State(TypedDict):
    query: str

    tasks: list[Task]

    shared_memory: dict[str, Any]

    final_answer: str