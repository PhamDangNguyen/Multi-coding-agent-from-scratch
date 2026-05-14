import json
from pathlib import Path
from typing import Any

CONFIG_DIR = Path(__file__).resolve().parent
ALLOWED_CONFIGS = {"orchestrator.json", "logging.json"}


def load_config(filename: str) -> dict[str, Any]:
    """Load a whitelisted JSON config from configs/."""
    if filename not in ALLOWED_CONFIGS:
        allowed = ", ".join(sorted(ALLOWED_CONFIGS))
        raise ValueError(f"Unsupported config '{filename}'. Choose one of: {allowed}")

    with (CONFIG_DIR / filename).open("r", encoding="utf-8") as file:
        return json.load(file)

__all__ = ["load_config"]
