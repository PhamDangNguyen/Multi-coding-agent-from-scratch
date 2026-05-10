# tools/git_diff.py

import subprocess
from tools.base import BaseTool


class GitDiffTool(BaseTool):
    name = "git_diff"
    description = "Show git diff"
    title = "Git Diff"

    async def execute(self):
        result = subprocess.run(
            ["git", "diff"],
            capture_output=True,
            text=True
        )

        return result.stdout