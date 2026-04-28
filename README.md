# Mutil agent from scratch 
This repository builds a multi-agent system step by step in order to solve problems that a single agent typically faces.
# Proposed Architecture
```bash
multi-agent-system/
│
├── orchestrator/               # Center brain
│   ├── orchestrator.py         # agent
│   ├── planner.py              # planning logic
│   ├── feedback.py             # self-reflection / critic loop
│   └── state.py                # global task state
│
├── logging/                    # logging setting 
│
├── mcp/                        # mcp setup   
│
├── llm/                        # LLM provider init 
│   ├── provider         
│   │   ├── ....
│   ├── base.py     
│
├── agents/                     # implements agent
│   ├── base.py
│   ├── coding_agent.py
│   ├── retrieval_agent.py
│   └── citation_agent.py
│
├── protocol/                   # multi-agent protocol
│   ├── registry.py             # discovery - agent subscription 
│   ├── dispatcher.py           # deliver task to each agent
│   ├── message.py              # message passing
│   └── capability.py           # agent capabilities 
│
├── tools/                      # common tools
│   ├── web_search.py
│   ├── code_executor.py
│   └── db.py
│
├── memory/                     # memory system
│   ├── short_term.py
│   ├── long_term.py
│   └── vector_store.py
│
├── prompts/                    # prompt
│   ├── orchestrator/
│   ├── agents/
│   │   ├── coding.md
│   │   ├── retrieval.md
│   │   └── citation.md
│   │
│   ├── llm_systems/
│   │   ├── gemini.md
│   │   ├── openai.md
│
├── schemas/                    # contract IO
│   ├── task.py
│   ├── message.py
│   └── agent_output.py
│
├── workflows/                  #  concrete flow
│   ├── qa_flow.py
│   ├── coding_flow.py
│   └── research_flow.py
│
├── services/                   # API layer
│   ├── api.py
│   └── worker.py
│
├── configs/
├── utils/
├── tests/
│
├── main.py
└── README.md
```
- The target flow for building an agentic AI is as follows:  
![Agentic flow](imgs/1.jpeg)
# Prequisite
## Environment Setup 
- Install [UV](https://docs.astral.sh/uv/getting-started/installation/) or [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install/overview) to create environments for this project. For now, I choose uv for its convenience.
