# tools/run_command.py

import subprocess
from tools.base import BaseTool


class RunCommandTool(BaseTool):
    name = "run_command"
    description = "Run shell command"
    title = "Run Command"

    async def execute(self, command: str):
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }