"""Simple agents initializer.

Import explicit agent modules and register instances into `Agent_farm`.
"""
from typing import Dict

from .base import BaseAgent

Agent_farm: Dict[str, BaseAgent] = {}

# Explicit imports of available agents
from .project_architect_agent import ProjectArchitectAgent
from .coding_agent import CodingAgent
from .test_agent import TestAgent
from .code_review_agent import CodeReviewAgent


for AgentCls in (ProjectArchitectAgent, CodingAgent, TestAgent, CodeReviewAgent):
    if issubclass(AgentCls, ProjectArchitectAgent):
        print("Đúng là ProjectArchitectAgent")
    else:
        inst = AgentCls()
        inst.subscribe(Agent_farm)


__all__ = ["Agent_farm"]
