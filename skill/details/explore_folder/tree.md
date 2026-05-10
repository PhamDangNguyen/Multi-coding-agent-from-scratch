# Tree Generation Script

## tree.py

```python
"""
Tree generation script - Display directory structure as a tree
"""

import os
from pathlib import Path
from typing import Optional, Set, List


class TreeGenerator:
    """Generate a visual tree representation of directory structure"""
    
    DEFAULT_IGNORE = {
        '.git', '__pycache__', '.venv', '.env', 'node_modules',
        '.pytest_cache', '.mypy_cache', 'venv', 'env',
        '.egg-info', 'dist', 'build', '.idea', '.vscode'
    }
    
    def __init__(self, ignore_patterns: Optional[Set[str]] = None, max_depth: Optional[int] = None):
        """
        Initialize tree generator
        
        Args:
            ignore_patterns: Set of directory/file names to ignore (defaults to DEFAULT_IGNORE)
            max_depth: Maximum depth to traverse (None for unlimited)
        """
        self.ignore_patterns = ignore_patterns or self.DEFAULT_IGNORE.copy()
        self.max_depth = max_depth
        self.lines: List[str] = []
    
    def should_ignore(self, name: str) -> bool:
        """Check if a path should be ignored"""
        return any(pattern in name for pattern in self.ignore_patterns)
    
    def generate(self, root_path: str) -> str:
        """Generate tree for a given path"""
        root = Path(root_path)
        
        if not root.exists():
            return f"Path not found: {root_path}"
        
        self.lines = []
        self.lines.append(f"{root.name}/")
        
        self._traverse(root, "", 0)
        
        return "\n".join(self.lines)
    
    def _traverse(self, current_path: Path, prefix: str, depth: int):
        """Recursively traverse directory"""
        if self.max_depth is not None and depth >= self.max_depth:
            return
        
        try:
            contents = sorted(current_path.iterdir(), 
                            key=lambda x: (not x.is_dir(), x.name.lower()))
        except (PermissionError, OSError):
            return
        
        # Filter ignored items
        contents = [x for x in contents if not self.should_ignore(x.name)]
        
        for i, item in enumerate(contents):
            is_last = i == len(contents) - 1
            current_prefix = "└── " if is_last else "├── "
            next_prefix = "    " if is_last else "│   "
            
            # Format item name
            if item.is_dir():
                display_name = f"{item.name}/"
            else:
                display_name = item.name
            
            self.lines.append(f"{prefix}{current_prefix}{display_name}")
            
            # Recursively process directories
            if item.is_dir() and not self.should_ignore(item.name):
                self._traverse(item, prefix + next_prefix, depth + 1)


def generate_tree(path: str, ignore_patterns: Optional[Set[str]] = None, 
                 max_depth: Optional[int] = None) -> str:
    """
    Generate a tree representation of a directory
    
    Args:
        path: Root directory path
        ignore_patterns: Set of patterns to ignore
        max_depth: Maximum depth to traverse
    
    Returns:
        String representation of the tree
    
    Example:
        >>> tree = generate_tree("/home/user/project", max_depth=2)
        >>> print(tree)
    """
    generator = TreeGenerator(ignore_patterns, max_depth)
    return generator.generate(path)


if __name__ == "__main__":
    import sys
    
    # Usage: python tree.py [path] [--max-depth N] [--ignore pattern1,pattern2]
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    
    max_depth = None
    ignore_patterns = None
    
    # Parse arguments
    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == "--max-depth" and i + 1 < len(sys.argv):
            max_depth = int(sys.argv[i + 1])
        elif arg == "--ignore" and i + 1 < len(sys.argv):
            ignore_patterns = set(sys.argv[i + 1].split(","))
    
    tree = generate_tree(path, ignore_patterns, max_depth)
    print(tree)
```

## Usage Examples

```bash
python tree.py /path/to/folder
python tree.py /path/to/folder --max-depth 2
python tree.py /path/to/folder --ignore ".git,__pycache__,node_modules"
```
