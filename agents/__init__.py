"""Simple agents initializer.

Import explicit agent modules and register instances into `Agent_farm`.
"""
from typing import Dict, Any
import os

from llm.provider.openai_langchain import OpenAIClientLangChain
from llm.provider.gemini_langchain import GeminiClientLangChain
from schemas.orchestrator.config import OrchestratorConfig
from .base import BaseAgent
# Explicit imports of available agents
from .project_architect_agent import ProjectArchitectAgent
from .coding_agent import CodingAgent
from .test_agent import TestAgent
from .review_agent import ReviewAgent
from .documentation_agent import DocumentationAgent
from .summary_agent import SummaryAgent
from orchestrator_flow.planner import AgentPlanner
from log_set import AppLogger
logger = AppLogger(__name__)
AgentClass = type[Any]

def build_llm(config: OrchestratorConfig) -> Any:
    provider = config.provider.lower()
    if provider == "openai":
        from llm.provider.openai_langchain import OpenAIClientLangChain
        api_key, model = os.getenv("OPENAI_API"), os.getenv("OPENAI_MODEL")
        if not api_key:
            raise RuntimeError("Missing OPENAI_API or OPENAI_API_KEY")
        return OpenAIClientLangChain(api_key=api_key, model=model)
    if provider == "gemini":
        from llm.provider.gemini_langchain import GeminiClientLangChain
        api_key, model = os.getenv("GEMINI_API"), os.getenv("GEMINI_MODEL")
        if not api_key:
            raise RuntimeError("Missing GEMINI_API, GEMINI_API_KEY, or GOOGLE_API_KEY")
        return GeminiClientLangChain(api_key=api_key, model=model)
    raise RuntimeError(f"Unsupported LLM_PROVIDER: {config.provider}")

def build_farm_agents(llm_client: OpenAIClientLangChain | GeminiClientLangChain) -> Dict[str, BaseAgent]:
    Agent_farm = {}
    for AgentCls in (ProjectArchitectAgent, CodingAgent, TestAgent, ReviewAgent, DocumentationAgent):
        inst = AgentCls(llm_client)
        inst.subscribe(Agent_farm)
    logger.log("INFO", f"Initializing agents and registering to Agent farming ... {list(Agent_farm.keys())}")
    return Agent_farm


def load_default_agent_instances(
    llm_client: OpenAIClientLangChain | GeminiClientLangChain,
) -> dict[str, Any]:
    logger.log("INFO", "Loading available agent instances ...")

    classes = (
        ProjectArchitectAgent,
        CodingAgent,
        TestAgent,
        ReviewAgent,
        DocumentationAgent,
        AgentPlanner,
        SummaryAgent
    )

    agent_farm = build_farm_agents(llm_client)

    return {
        AgentCls.agent_name: (
            AgentCls(llm_client, agent_farm=agent_farm)
            if AgentCls is AgentPlanner
            else AgentCls(llm_client)
        )
        for AgentCls in classes
    }

__all__ = ["build_farm_agents", "load_default_agent_instances", "build_llm", "AgentClass"]
