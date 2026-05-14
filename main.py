from orchestrator_flow.orchestrator import MultiAgentOrchestrator, run 
import asyncio

from schemas.orchestrator.config import OrchestratorConfig
from agents import load_default_agent_instances, build_llm
from rich import print

if __name__ == "__main__":
    from rich import print
    llm_client = build_llm(OrchestratorConfig())
    orchestrator= MultiAgentOrchestrator(config=OrchestratorConfig(), agent_classes=load_default_agent_instances(llm_client))
    query = "Tại thư mục này tạo folder code_test để  code một API tính cộng 2 số bằng python đơn giản theo pattern design."
    output = asyncio.run(run(query, orchestrator=orchestrator))
    print(output["final_answer"])