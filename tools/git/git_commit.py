# tools/git_commit.py

import subprocess
from tools.base import BaseTool


class GitCommitTool(BaseTool):
    name = "git_commit"
    description = "Create git commit"
    title = "Git Commit"

    async def execute(self, message: str):
        result = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True,
            text=True
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }