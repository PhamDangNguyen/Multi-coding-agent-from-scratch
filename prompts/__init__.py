from __future__ import annotations
from functools import lru_cache
from pathlib import Path

_PROMPTS_DIR = Path(__file__).parent

# print(f"Loading prompts from: {_PROMPTS_DIR}")

@lru_cache
def load_prompt(filename: str) -> str:
    """Return the prompt text stored in the given Markdown file."""

    return (_PROMPTS_DIR / filename).read_text(encoding="utf-8").strip()