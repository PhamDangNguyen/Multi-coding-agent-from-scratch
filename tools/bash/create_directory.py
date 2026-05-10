# tools/create_directory.py

import os
from tools.base import BaseTool


class CreateDirectoryTool(BaseTool):
    name = "create_directory"
    description = "Create a directory"
    title = "Create Directory"

    async def execute(self, path: str):
        os.makedirs(path, exist_ok=True)

        return f"Directory created successfully: {path}"