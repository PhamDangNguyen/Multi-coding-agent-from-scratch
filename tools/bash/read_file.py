# tools/bash/read_file.py

from tools.base import BaseTool

class ReadFileTool(BaseTool):
    name = "read_file"
    description = "Read content from file"
    title = "Read File"

    async def execute(self, path: str):
        with open(path) as f:
            return f.read()