"""Simple agents initializer.

Import explicit agent modules and register instances into `Agent_farm`.
"""
from typing import Dict

from .base import BaseAgent

Agent_farm: Dict[str, BaseAgent] = {}

# Explicit imports of available agents
from .bash_agent import BashAgent
from .coding_agent import CodingAgent


for AgentCls in (BashAgent, CodingAgent):
    inst = AgentCls()
    inst.subscribe(Agent_farm)


__all__ = ["Agent_farm"]
