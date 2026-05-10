# tools/list_directory.py

import os
from tools.base import BaseTool


class ListDirectoryTool(BaseTool):
    name = "list_directory"
    description = "List files and folders in a directory"
    title = "List Directory"

    async def execute(self, path: str = "."):
        return os.listdir(path)