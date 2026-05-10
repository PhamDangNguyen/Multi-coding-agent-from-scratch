# tools/move_file.py

import shutil
from tools.base import BaseTool


class MoveFileTool(BaseTool):
    name = "move_file"
    description = "Move a file"
    title = "Move File"

    async def execute(self, src: str, dst: str):
        shutil.move(src, dst)

        return f"File moved successfully from {src} to {dst}"