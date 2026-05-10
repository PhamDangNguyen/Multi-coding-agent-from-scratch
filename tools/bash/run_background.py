# tools/run_background.py

import subprocess
from tools.base import BaseTool


class RunBackgroundTool(BaseTool):
    name = "run_background"
    description = "Run command in background"
    title = "Run Background"

    async def execute(self, command: str):
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        return {
            "pid": process.pid,
            "message": f"Process started in background: {process.pid}"
        }