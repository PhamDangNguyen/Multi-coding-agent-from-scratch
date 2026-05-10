# tools/copy_file.py

import shutil
from tools.base import BaseTool


class CopyFileTool(BaseTool):
    name = "copy_file"
    description = "Copy a file"
    title = "Copy File"

    async def execute(self, src: str, dst: str):
        shutil.copy(src, dst)

        return f"File copied successfully from {src} to {dst}"