from typing import Literal, TypedDict, Any
from pydantic import BaseModel
from dataclasses import dataclass
from configs import load_config

orchestrator_config = load_config("orchestrator.json")
class OrchestratorConfig(BaseModel):
    provider: str = orchestrator_config.get("provider", "openai")
    model: str | None = orchestrator_config.get("model")
    max_iterations: int = orchestrator_config.get("max_iterations_per_agent", 5)
    planner_timeout_seconds: float | None = orchestrator_config.get("planner_timeout_seconds", 90.0)
    task_timeout_seconds: float | None = orchestrator_config.get("task_timeout_seconds", 180.0)
    max_tasks: int = orchestrator_config.get("max_tasks", 20)
    stop_on_failure: bool = orchestrator_config.get("stop_on_failure", False)
