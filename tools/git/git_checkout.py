# tools/git_checkout.py

import subprocess
from tools.base import BaseTool


class GitCheckoutTool(BaseTool):
    name = "git_checkout"
    description = "Checkout git branch"
    title = "Git Checkout"

    async def execute(self, branch: str):
        result = subprocess.run(
            ["git", "checkout", branch],
            capture_output=True,
            text=True
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }