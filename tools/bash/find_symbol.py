# tools/find_symbol.py

from pathlib import Path
from tools.base import BaseTool


class FindSymbolTool(BaseTool):
    name = "find_symbol"
    description = "Find symbol or text inside files"
    title = "Find Symbol"

    async def execute(self, name: str, root: str = "."):
        matches = []

        for path in Path(root).rglob("*"):
            if path.is_file():
                try:
                    content = path.read_text(errors="ignore")

                    if name in content:
                        matches.append(str(path))

                except Exception:
                    pass

        return matches