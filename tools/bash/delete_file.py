# tools/delete_file.py

import os
from tools.base import BaseTool


class DeleteFileTool(BaseTool):
    name = "delete_file"
    description = "Delete a file"
    title = "Delete File"

    async def execute(self, path: str):
        os.remove(path)

        return f"File deleted successfully: {path}"