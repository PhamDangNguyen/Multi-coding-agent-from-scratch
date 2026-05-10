# tools/bash/write_files.py

from tools.base import BaseTool


class WriteFileTool(BaseTool):
    name = "write_file"
    description = "Write content to file"
    title = "Write File"

    async def execute(self, path: str, content: str):
        with open(path, "w") as f:
            f.write(content)

        return f"File written successfully: {path}"