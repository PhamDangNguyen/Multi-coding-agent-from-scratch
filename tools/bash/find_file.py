# tools/find_files.py

from pathlib import Path
from tools.base import BaseTool


class FindFilesTool(BaseTool):
    name = "find_files"
    description = "Find files by pattern"
    title = "Find Files"

    async def execute(self, pattern: str, root: str = "."):
        return [
            str(path)
            for path in Path(root).rglob(pattern)
        ]