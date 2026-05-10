import subprocess
from pathlib import Path
from typing import List, Dict, Optional


class GitFileManager:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
    
    def is_git_repo(self) -> bool:
        try:
            subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.repo_path,
                capture_output=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def list_tracked_files(self) -> List[str]:
        try:
            result = subprocess.run(
                ["git", "ls-files"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip().split('\n') if result.stdout.strip() else []
        except (subprocess.CalledProcessError, FileNotFoundError):
            return []
    
    def list_untracked_files(self) -> List[str]:
        try:
            result = subprocess.run(
                ["git", "ls-files", "-o", "--exclude-standard"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip().split('\n') if result.stdout.strip() else []
        except (subprocess.CalledProcessError, FileNotFoundError):
            return []
    
    def list_staged_files(self) -> List[str]:
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip().split('\n') if result.stdout.strip() else []
        except (subprocess.CalledProcessError, FileNotFoundError):
            return []


def list_git_files(repo_path: str = ".") -> List[str]:
    manager = GitFileManager(repo_path)
    return manager.list_tracked_files()
