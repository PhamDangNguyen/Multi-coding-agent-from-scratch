# tools/ls.py

import os
from tools.base import BaseTool


class LsTool(BaseTool):
    name = "ls"
    description = "List current directory content"
    title = "LS"

    async def execute(self):
        return os.listdir(".")