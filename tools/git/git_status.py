# tools/git_status.py

import subprocess
from tools.base import BaseTool


class GitStatusTool(BaseTool):
    name = "git_status"
    description = "Get git repository status"
    title = "Git Status"

    async def execute(self):
        result = subprocess.run(
            ["git", "status"],
            capture_output=True,
            text=True
        )

        return result.stdout