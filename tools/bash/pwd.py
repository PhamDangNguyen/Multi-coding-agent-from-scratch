# tools/pwd.py

import os
from tools.base import BaseTool


class PwdTool(BaseTool):
    name = "pwd"
    description = "Get current working directory"
    title = "PWD"

    async def execute(self):
        return os.getcwd()