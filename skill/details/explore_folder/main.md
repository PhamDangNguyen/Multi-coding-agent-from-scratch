# Main Explore Folder Integration

## explore_folder.py

This is the main integration script that combines all exploration tools.

```python
"""
Main exploration tool - Integration of all folder exploration capabilities
"""

from pathlib import Path
from typing import Optional, List, Dict
import os
import json


class ExplorerToolkit:
    """Complete toolkit for exploring directories"""
    
    def __init__(self, root_path: str):
        """Initialize explorer toolkit"""
        self.root_path = Path(root_path)
    
    def get_directory_info(self) -> Dict:
        """Get comprehensive directory information"""
        return {
            'path': str(self.root_path),
            'exists': self.root_path.exists(),
            'is_dir': self.root_path.is_dir(),
            'children': self._count_children(),
            'statistics': self._get_statistics(),
            'git_info': self._get_git_info() if self._is_git_repo() else None
        }
    
    def _count_children(self) -> Dict[str, int]:
        """Count files and directories"""
        files = 0
        dirs = 0
        
        try:
            for item in self.root_path.iterdir():
                if item.is_dir():
                    dirs += 1
                elif item.is_file():
                    files += 1
        except PermissionError:
            pass
        
        return {'files': files, 'directories': dirs}
    
    def _get_statistics(self) -> Dict:
        """Get statistics about directory contents"""
        stats = {
            'total_size': 0,
            'file_types': {},
            'largest_files': []
        }
        
        all_files = []
        
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                filepath = os.path.join(root, file)
                
                try:
                    size = os.path.getsize(filepath)
                    stats['total_size'] += size
                    all_files.append((filepath, size))
                    
                    ext = Path(file).suffix or 'no_extension'
                    stats['file_types'][ext] = stats['file_types'].get(ext, 0) + 1
                except OSError:
                    pass
        
        # Get largest files
        stats['largest_files'] = sorted(all_files, key=lambda x: x[1], reverse=True)[:5]
        
        return stats
    
    def _is_git_repo(self) -> bool:
        """Check if directory is a git repository"""
        git_dir = self.root_path / '.git'
        return git_dir.exists() or self._check_git_status()
    
    def _check_git_status(self) -> bool:
        """Check git status via command"""
        import subprocess
        try:
            subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                cwd=self.root_path,
                capture_output=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _get_git_info(self) -> Optional[Dict]:
        """Get git repository information"""
        import subprocess
        
        try:
            # Get current branch
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                cwd=self.root_path,
                capture_output=True,
                text=True,
                check=True
            )
            branch = result.stdout.strip()
            
            # Get tracked file count
            result = subprocess.run(
                ['git', 'ls-files'],
                cwd=self.root_path,
                capture_output=True,
                text=True,
                check=True
            )
            tracked_count = len(result.stdout.strip().split('\n'))
            
            return {
                'is_repo': True,
                'branch': branch,
                'tracked_files': tracked_count
            }
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None
    
    def generate_report(self) -> str:
        """Generate a complete exploration report"""
        info = self.get_directory_info()
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║             DIRECTORY EXPLORATION REPORT                     ║
╚══════════════════════════════════════════════════════════════╝

Path: {info['path']}
Exists: {info['exists']}
Is Directory: {info['is_dir']}

CONTENTS:
├── Files: {info['children']['files']}
└── Directories: {info['children']['directories']}

STATISTICS:
├── Total Size: {self._format_size(info['statistics']['total_size'])}
└── File Types: {len(info['statistics']['file_types'])} types

TOP 5 LARGEST FILES:
"""
        
        for i, (filepath, size) in enumerate(info['statistics']['largest_files'], 1):
            rel_path = Path(filepath).relative_to(self.root_path) if self.root_path in Path(filepath).parents else filepath
            report += f"{i}. {rel_path}: {self._format_size(size)}\n"
        
        if info['git_info']:
            report += f"""
GIT INFORMATION:
├── Branch: {info['git_info']['branch']}
└── Tracked Files: {info['git_info']['tracked_files']}
"""
        
        return report
    
    @staticmethod
    def _format_size(size: int) -> str:
        """Format bytes to human-readable size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"


def explore_folder(path: str) -> Dict:
    """Quick exploration function"""
    explorer = ExplorerToolkit(path)
    return explorer.get_directory_info()


if __name__ == "__main__":
    import sys
    
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    
    explorer = ExplorerToolkit(path)
    print(explorer.generate_report())
```

## Quick Start Guide

### 1. Explore by Visual Tree
```python
from scripts.tree import generate_tree
print(generate_tree("/home/user/project", max_depth=3))
```

### 2. Find Files
```python
from scripts.find import FileFinder

finder = FileFinder("/home/user/project")
python_files = finder.find_by_extension("py")
recent = finder.find_by_date(days=7)
```

### 3. Search Text Content
```python
from scripts.grep_search import TextSearcher

searcher = TextSearcher("/home/user/project")
results = searcher.search("TODO", file_pattern="*.py", context_lines=2)
```

### 4. Use Ripgrep
```bash
rg "search_term" /path/to/folder
rg -t py "error" .
rg -A 3 -B 3 "pattern" src/
```

### 5. Git Integration
```bash
git ls-files  # List tracked files
git ls-files -o --exclude-standard  # List untracked
git diff --name-status  # Show changed files
```

## All Available Functions

| Tool | Function | Purpose |
|------|----------|---------|
| Tree | `generate_tree()` | Display directory structure |
| Find | `FileFinder.find_by_extension()` | Find files by extension |
| | `FileFinder.find_by_size()` | Find files by size |
| | `FileFinder.find_duplicates()` | Find duplicate files |
| Search | `TextSearcher.search()` | Search text in files |
| Git | `GitFileManager.list_tracked_files()` | List git tracked files |
| | `GitFileManager.get_file_status()` | Get git file status |

## Workflow Examples

### Project Analysis
```python
explorer = ExplorerToolkit("/home/user/project")
print(explorer.generate_report())
```

### Code Refactoring
```python
searcher = TextSearcher("/home/user/project")
# Find all imports
imports = searcher.search("^import|^from", file_pattern="*.py")
```

### Cleanup
```python
finder = FileFinder("/home/user/project")
# Find large files
large = finder.find_by_size(min_size=10*1024*1024)
# Find old logs
logs = finder.find_by_date(days=-30)
```
