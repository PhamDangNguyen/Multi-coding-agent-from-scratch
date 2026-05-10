---
name: explore_folder
description: Use this skill whenever the user wants to explore, navigate, or understand the structure of directories and files. This includes listing directory contents, finding files by name or pattern, searching for text within files, viewing file hierarchies as trees, discovering folder structure, filtering files by type or criteria, and analyzing project layouts. Trigger when the user asks to "explore", "search", "find", "navigate", "understand structure", "what's in this folder", or references exploring a directory path.
license: Proprietary. LICENSE.txt has complete terms
---

# Directory Exploration Guide

## Overview

This guide covers essential directory and file exploration operations. Use these tools to understand folder structures, find specific files, search for content, and analyze project layouts.

## Quick Start

```python
from scripts.tree import generate_tree
from scripts.find import find_files
from scripts.grep_search import search_text

# Generate directory tree
tree = generate_tree("/path/to/folder")
print(tree)

# Find files by pattern
files = find_files("/path/to/folder", pattern="*.py")
print(files)

# Search for text in files
results = search_text("/path/to/folder", pattern="function_name")
print(results)
```

## Command-Line Tools

### 1. Tree - View Directory Hierarchy

Display the entire directory structure as a tree:

```bash
# Basic tree view
tree /path/to/folder

# Limit depth
tree -L 2 /path/to/folder

# Show file sizes
tree -h /path/to/folder

# Ignore certain directories
tree -I 'node_modules|.git' /path/to/folder

# Output to file
tree /path/to/folder > tree_output.txt
```

### 2. Find - Locate Files

Search for files by name, type, size, or modification time:

```bash
# Find all Python files
find /path/to/folder -name "*.py"

# Find files modified in last 7 days
find /path/to/folder -mtime -7

# Find files larger than 1MB
find /path/to/folder -size +1M

# Find and execute command
find /path/to/folder -name "*.log" -delete

# Find hidden files
find /path/to/folder -name ".*"

# Combine conditions (AND)
find /path/to/folder -name "*.py" -type f
```

### 3. Grep - Search Text Content

Search for patterns within files:

```bash
# Basic search
grep -r "search_term" /path/to/folder

# Case-insensitive search
grep -ri "search_term" /path/to/folder

# Show line numbers
grep -rn "search_term" /path/to/folder

# Show context lines
grep -rn -A 3 -B 3 "search_term" /path/to/folder

# Invert match (exclude pattern)
grep -rv "exclude_pattern" /path/to/folder

# Search specific file types
grep -r "search_term" /path/to/folder --include="*.py"

# Count matches
grep -r "search_term" /path/to/folder | wc -l
```

### 4. Ripgrep (rg) - Fast Text Search

A faster alternative to grep with better defaults:

```bash
# Basic search
rg "search_term" /path/to/folder

# Case-insensitive
rg -i "search_term" /path/to/folder

# Show line numbers and context
rg -n -A 3 -B 3 "search_term" /path/to/folder

# Search specific file types
rg -t py "search_term" /path/to/folder

# Exclude patterns
rg --glob "!*.log" "search_term" /path/to/folder

# Count matches
rg -c "search_term" /path/to/folder

# Show only filenames
rg -l "search_term" /path/to/folder
```

### 5. Git ls-files - List Tracked Files

Show files tracked by Git:

```bash
# List all tracked files
git ls-files

# List staged files
git ls-files -s

# List deleted files
git ls-files -d

# List untracked files
git ls-files -o --exclude-standard

# List files in specific directory
git ls-files | grep "directory/"

# Count tracked files
git ls-files | wc -l

# Show file status
git ls-files -s | grep -E "^[0-9]+ [a-z]+\s+[0-9]+\s+(.+)$"
```

## Python Scripts

### explore_directory.py

```python
import os
from pathlib import Path
from typing import List, Dict, Optional

def explore_directory(path: str, max_depth: int = None, ignore_patterns: List[str] = None) -> Dict:
    """
    Explore a directory and return its structure.
    
    Args:
        path: Directory path to explore
        max_depth: Maximum depth to traverse (None for unlimited)
        ignore_patterns: List of patterns to ignore (e.g., ['.git', '__pycache__'])
    
    Returns:
        Dictionary with directory structure information
    """
    if ignore_patterns is None:
        ignore_patterns = ['.git', '__pycache__', '.venv', 'node_modules']
    
    path = Path(path)
    structure = {
        'name': path.name,
        'path': str(path),
        'type': 'directory',
        'children': [],
        'file_count': 0,
        'dir_count': 0
    }
    
    def traverse(current_path: Path, current_depth: int = 0):
        if max_depth is not None and current_depth >= max_depth:
            return
        
        try:
            items = sorted(current_path.iterdir())
        except PermissionError:
            return
        
        for item in items:
            if any(pattern in item.name for pattern in ignore_patterns):
                continue
            
            if item.is_file():
                structure['file_count'] += 1
                structure['children'].append({
                    'name': item.name,
                    'path': str(item),
                    'type': 'file',
                    'size': item.stat().st_size
                })
            elif item.is_dir():
                structure['dir_count'] += 1
                traverse(item, current_depth + 1)
    
    traverse(path)
    return structure

# Example usage
if __name__ == "__main__":
    result = explore_directory("/path/to/folder", max_depth=3)
    import json
    print(json.dumps(result, indent=2))
```

### find_duplicates.py

```python
import os
from pathlib import Path
from collections import defaultdict
import hashlib

def find_duplicates(path: str, by_size: bool = True) -> Dict[str, List[str]]:
    """Find duplicate files by size or content hash"""
    
    duplicates = defaultdict(list)
    
    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            if by_size:
                size = os.path.getsize(filepath)
                duplicates[size].append(filepath)
            else:
                with open(filepath, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                    duplicates[file_hash].append(filepath)
    
    return {k: v for k, v in duplicates.items() if len(v) > 1}

# Example usage
if __name__ == "__main__":
    dups = find_duplicates("/path/to/folder")
    for key, files in dups.items():
        print(f"Potential duplicates ({len(files)}):")
        for f in files:
            print(f"  - {f}")
```

### analyze_folder_stats.py

```python
import os
from pathlib import Path
from collections import defaultdict

def analyze_folder(path: str) -> Dict:
    """Generate statistics about a folder"""
    
    stats = {
        'total_files': 0,
        'total_dirs': 0,
        'total_size': 0,
        'by_extension': defaultdict(int),
        'by_size': defaultdict(int),
        'largest_files': []
    }
    
    all_files = []
    
    for root, dirs, files in os.walk(path):
        stats['total_dirs'] += len(dirs)
        for file in files:
            filepath = os.path.join(root, file)
            stats['total_files'] += 1
            
            ext = Path(file).suffix or 'no_extension'
            stats['by_extension'][ext] += 1
            
            try:
                size = os.path.getsize(filepath)
                stats['total_size'] += size
                all_files.append((filepath, size))
            except OSError:
                pass
    
    # Get 10 largest files
    stats['largest_files'] = sorted(all_files, key=lambda x: x[1], reverse=True)[:10]
    
    return stats

# Example usage
if __name__ == "__main__":
    stats = analyze_folder("/path/to/folder")
    print(f"Total files: {stats['total_files']}")
    print(f"Total directories: {stats['total_dirs']}")
    print(f"Total size: {stats['total_size'] / (1024*1024):.2f} MB")
    print(f"\nFile types:")
    for ext, count in stats['by_extension'].items():
        print(f"  {ext}: {count}")
    print(f"\nLargest files:")
    for file, size in stats['largest_files']:
        print(f"  {file}: {size / (1024*1024):.2f} MB")
```

## Practical Examples

### Find all Python files in a project

```bash
find . -name "*.py" -type f | head -20
```

### Search for a specific function definition

```bash
rg -n "def my_function" src/
```

### List files modified today

```bash
find . -type f -mtime 0
```

### Show code statistics

```bash
find . -name "*.py" -type f | xargs wc -l | sort -n
```

### Find and list file sizes recursively

```bash
find . -type f -exec ls -lh {} \; | awk '{print $5, $9}' | sort -k1 -rn
```

### Search across multiple file types

```bash
rg -t py -t js "TODO|FIXME" .
```

## Best Practices

1. **Use .gitignore patterns**: Exclude common directories like `.git`, `node_modules`, `__pycache__`
2. **Limit search scope**: Always specify a directory to avoid searching system paths
3. **Use ripgrep for speed**: `rg` is significantly faster than `grep` for large codebases
4. **Save results**: Redirect output to files for large searches: `find ... > results.txt`
5. **Combine tools**: Chain commands with pipes for powerful exploration: `find . -name "*.py" | xargs grep "pattern"`
6. **Regular expressions**: Use regex patterns for complex searches in `grep` and `rg`

## See Also

- [reference.md](reference.md) - Advanced usage patterns and examples
- LICENSE.txt - Terms of use
