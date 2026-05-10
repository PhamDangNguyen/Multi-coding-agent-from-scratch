# Find Files Script

## find.py

```python
"""
Find files by various criteria - name, pattern, size, modification time, etc.
"""

import os
from pathlib import Path
from typing import Optional, List, Callable
from datetime import datetime, timedelta
import fnmatch


class FileFinder:
    """Find files by various criteria"""
    
    def __init__(self, root_path: str):
        """
        Initialize file finder
        
        Args:
            root_path: Root directory to search from
        """
        self.root_path = Path(root_path)
    
    def find_by_name(self, pattern: str, exclude_hidden: bool = False) -> List[str]:
        """
        Find files by name pattern (glob style)
        
        Args:
            pattern: Glob pattern (e.g., "*.py", "test_*")
            exclude_hidden: Exclude hidden files starting with .
        
        Returns:
            List of file paths matching the pattern
        """
        matches = []
        
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                if exclude_hidden and file.startswith('.'):
                    continue
                
                if fnmatch.fnmatch(file, pattern):
                    full_path = os.path.join(root, file)
                    matches.append(full_path)
        
        return sorted(matches)
    
    def find_by_extension(self, *extensions: str) -> List[str]:
        """
        Find files by extension(s)
        
        Args:
            *extensions: Extensions to search for (e.g., "py", "md", "txt")
        
        Returns:
            List of file paths with matching extensions
        """
        matches = []
        
        # Normalize extensions (add . if missing)
        exts = [f".{ext}" if not ext.startswith('.') else ext for ext in extensions]
        
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                if Path(file).suffix in exts:
                    full_path = os.path.join(root, file)
                    matches.append(full_path)
        
        return sorted(matches)
    
    def find_by_size(self, min_size: int = None, max_size: int = None) -> List[tuple]:
        """
        Find files by size range
        
        Args:
            min_size: Minimum file size in bytes (None for no limit)
            max_size: Maximum file size in bytes (None for no limit)
        
        Returns:
            List of (filepath, size) tuples
        """
        matches = []
        
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                full_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(full_path)
                    
                    if min_size and size < min_size:
                        continue
                    if max_size and size > max_size:
                        continue
                    
                    matches.append((full_path, size))
                except OSError:
                    pass
        
        return sorted(matches, key=lambda x: x[1], reverse=True)
    
    def find_by_date(self, days: int = None, from_date: str = None) -> List[tuple]:
        """
        Find files modified within time range
        
        Args:
            days: Number of days (e.g., 7 for files modified in last 7 days)
            from_date: Start date in format YYYY-MM-DD
        
        Returns:
            List of (filepath, modified_date) tuples
        """
        matches = []
        
        if days:
            cutoff = datetime.now() - timedelta(days=days)
        elif from_date:
            cutoff = datetime.strptime(from_date, "%Y-%m-%d")
        else:
            return matches
        
        cutoff_timestamp = cutoff.timestamp()
        
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                full_path = os.path.join(root, file)
                try:
                    mtime = os.path.getmtime(full_path)
                    if mtime >= cutoff_timestamp:
                        mod_date = datetime.fromtimestamp(mtime)
                        matches.append((full_path, mod_date))
                except OSError:
                    pass
        
        return sorted(matches, key=lambda x: x[1], reverse=True)
    
    def find_duplicates(self, by_name: bool = True) -> dict:
        """
        Find duplicate files
        
        Args:
            by_name: If True, find by filename; if False, find by content hash
        
        Returns:
            Dictionary of duplicates {key: [files]}
        """
        import hashlib
        from collections import defaultdict
        
        duplicates = defaultdict(list)
        
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                full_path = os.path.join(root, file)
                
                if by_name:
                    key = file
                else:
                    try:
                        with open(full_path, 'rb') as f:
                            key = hashlib.md5(f.read()).hexdigest()
                    except (OSError, IOError):
                        continue
                
                duplicates[key].append(full_path)
        
        # Return only actual duplicates (count > 1)
        return {k: v for k, v in duplicates.items() if len(v) > 1}


def find_files(root_path: str, pattern: str = None, extension: str = None,
              min_size: int = None, max_size: int = None) -> List[str]:
    """
    Convenient function to find files with various criteria
    
    Args:
        root_path: Root directory to search
        pattern: Glob pattern for filename
        extension: File extension to search for
        min_size: Minimum file size in bytes
        max_size: Maximum file size in bytes
    
    Returns:
        List of matching file paths
    """
    finder = FileFinder(root_path)
    
    if extension:
        return finder.find_by_extension(extension)
    elif pattern:
        return finder.find_by_name(pattern)
    elif min_size or max_size:
        return [f for f, _ in finder.find_by_size(min_size, max_size)]
    
    return []


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python find.py <path> [--name pattern] [--ext extension] [--size min:max]")
        sys.exit(1)
    
    root = sys.argv[1]
    finder = FileFinder(root)
    
    # Parse arguments
    pattern = None
    extension = None
    
    for i, arg in enumerate(sys.argv[2:]):
        if arg == "--name" and i + 2 < len(sys.argv):
            pattern = sys.argv[i + 3]
        elif arg == "--ext" and i + 2 < len(sys.argv):
            extension = sys.argv[i + 3]
    
    if extension:
        results = finder.find_by_extension(extension)
    elif pattern:
        results = finder.find_by_name(pattern)
    else:
        results = []
    
    for result in results[:20]:  # Show first 20 results
        print(result)
    
    if len(results) > 20:
        print(f"... and {len(results) - 20} more")
```

## Usage Examples

```bash
# Find all Python files
python find.py /path/to/folder --ext py

# Find files matching pattern
python find.py /path/to/folder --name "test_*.py"

# Find large files
python find.py /path/to/folder --size "10M:"
```

## Integration with main script

```python
from find import FileFinder

finder = FileFinder("/home/user/project")
python_files = finder.find_by_extension("py")
large_files = finder.find_by_size(min_size=1024*1024)  # > 1MB
recent_files = finder.find_by_date(days=7)  # Last 7 days
duplicates = finder.find_duplicates(by_name=True)
```
