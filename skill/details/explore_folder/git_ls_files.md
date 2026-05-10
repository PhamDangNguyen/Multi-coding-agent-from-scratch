# Git ls-files Guide

## Overview

`git ls-files` shows information about files in the index and the working tree. It's useful for understanding which files are tracked, staged, or have conflicts.

## Basic Usage

```bash
# List all tracked files
git ls-files

# List files recursively with tree structure
git ls-files --full-name | head -20

# Count tracked files
git ls-files | wc -l
```

## File Status

```bash
# Show staged changes (-s = show object name and mode)
git ls-files -s

# Show deleted files
git ls-files -d

# Show untracked files
git ls-files -o --exclude-standard

# Show other files (untracked)
git ls-files -o
```

## Advanced Options

### Filter by Path

```bash
# Files in specific directory
git ls-files | grep "^src/"

# Files matching pattern
git ls-files | grep "\.py$"

# Exclude certain files
git ls-files | grep -v "node_modules"
```

### Show Modifications

```bash
# Modified files (compared to HEAD)
git diff --name-only

# Files with differences
git diff --name-status

# Staged files
git diff --name-only --cached
```

### Conflict Resolution

```bash
# Show conflicted files
git ls-files -u

# Files with merge conflicts
git ls-files --unmerged
```

## Python Integration

### git_integration.py

```python
"""
Git integration - List and analyze tracked files
"""

import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Set
import os


class GitFileManager:
    """Manage and query git tracked files"""
    
    def __init__(self, repo_path: str = "."):
        """
        Initialize git file manager
        
        Args:
            repo_path: Path to git repository
        """
        self.repo_path = Path(repo_path)
    
    def is_git_repo(self) -> bool:
        """Check if path is a git repository"""
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
        """Get all tracked files"""
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
        """Get untracked files"""
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
        """Get staged files"""
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
    
    def list_modified_files(self) -> List[str]:
        """Get modified but unstaged files"""
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip().split('\n') if result.stdout.strip() else []
        except (subprocess.CalledProcessError, FileNotFoundError):
            return []
    
    def get_file_status(self) -> Dict[str, List[str]]:
        """Get comprehensive file status"""
        return {
            'staged': self.list_staged_files(),
            'modified': self.list_modified_files(),
            'untracked': self.list_untracked_files(),
            'tracked': self.list_tracked_files()
        }
    
    def get_files_by_type(self, file_type: str) -> List[str]:
        """Get tracked files by type"""
        tracked = self.list_tracked_files()
        return [f for f in tracked if f.endswith(f".{file_type}")]
    
    def get_files_in_directory(self, directory: str) -> List[str]:
        """Get tracked files in a directory"""
        tracked = self.list_tracked_files()
        return [f for f in tracked if f.startswith(f"{directory}/")]
    
    def get_file_info(self, filepath: str) -> Dict:
        """Get detailed info about a git-tracked file"""
        try:
            result = subprocess.run(
                ["git", "ls-files", "-s", filepath],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse output format: [mode] [object] [stage] [file]
            if result.stdout.strip():
                parts = result.stdout.strip().split()
                return {
                    'mode': parts[0],
                    'object': parts[1],
                    'stage': parts[2],
                    'file': parts[3] if len(parts) > 3 else filepath,
                    'tracked': True
                }
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        return {'file': filepath, 'tracked': False}
    
    def get_git_status_summary(self) -> str:
        """Get a summary of git status"""
        status = self.get_file_status()
        
        summary = f"""
Git Repository Summary:
- Tracked files: {len(status['tracked'])}
- Staged changes: {len(status['staged'])}
- Modified files: {len(status['modified'])}
- Untracked files: {len(status['untracked'])}
"""
        return summary


def list_git_files(repo_path: str = ".") -> List[str]:
    """Convenience function to list git tracked files"""
    manager = GitFileManager(repo_path)
    return manager.list_tracked_files()


if __name__ == "__main__":
    import sys
    
    repo = sys.argv[1] if len(sys.argv) > 1 else "."
    
    manager = GitFileManager(repo)
    
    if not manager.is_git_repo():
        print(f"Not a git repository: {repo}")
        sys.exit(1)
    
    print(manager.get_git_status_summary())
    
    print("\nTracked files by type:")
    for ext in ["py", "md", "js", "json"]:
        files = manager.get_files_by_type(ext)
        if files:
            print(f"  .{ext}: {len(files)} files")
```

## Useful Aliases

Add to `.gitconfig`:

```ini
[alias]
    lsf = ls-files
    track-stats = !git ls-files | xargs wc -l | sort -n
    tracked-dirs = !git ls-files | cut -d/ -f1 | sort | uniq -c
    file-count = !git ls-files | wc -l
    untracked = ls-files -o --exclude-standard
    conflicts = diff --name-only --diff-filter=U
```

## Common Workflows

### Count Files by Type

```bash
git ls-files | sed 's/.*\.//' | sort | uniq -c | sort -rn
```

### Find Large Files

```bash
git ls-files -s | awk '{print $4}' | xargs -I {} sh -c 'echo "$(git cat-file -s {}| awk "{sum+=\$1} END {print sum}") bytes: {}"' | sort -rn | head -10
```

### Statistics

```bash
# Total lines of code
git ls-files | xargs wc -l | tail -1

# Files per directory
git ls-files | cut -d'/' -f1 | sort | uniq -c

# Show recent commits for tracked files
git log --name-status --oneline -10
```

## See Also

- [Git Documentation](https://git-scm.com/docs/git-ls-files)
- [Git Aliases](https://git-scm.com/book/en/v2/Git-Basics-Git-Aliases)
