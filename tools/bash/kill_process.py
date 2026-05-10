# tools/kill_process.py

import os
import signal
from tools.base import BaseTool


class KillProcessTool(BaseTool):
    name = "kill_process"
    description = "Kill process by PID"
    title = "Kill Process"

    async def execute(self, pid: int):
        os.kill(pid, signal.SIGTERM)

        return f"Process killed successfully: {pid}"