# Text Search Script

## grep_search.py

```python
"""
Text search across files - Basic grep functionality with patterns
"""

import os
import re
from pathlib import Path
from typing import Optional, List, Tuple, Pattern


class TextSearcher:
    """Search for text patterns in files"""
    
    def __init__(self, root_path: str, case_sensitive: bool = False):
        """
        Initialize text searcher
        
        Args:
            root_path: Root directory to search from
            case_sensitive: Whether search is case-sensitive
        """
        self.root_path = Path(root_path)
        self.case_sensitive = case_sensitive
    
    def search(self, pattern: str, file_pattern: str = "*", 
              context_lines: int = 0) -> List[dict]:
        """
        Search for text pattern in files
        
        Args:
            pattern: Text pattern or regex to search for
            file_pattern: Glob pattern for files to search (e.g., "*.py")
            context_lines: Number of context lines to include (0 for none)
        
        Returns:
            List of dicts with: {file, line_num, line, context}
        """
        results = []
        regex_flags = 0 if self.case_sensitive else re.IGNORECASE
        
        try:
            regex = re.compile(pattern, regex_flags)
        except re.error:
            # If pattern is not valid regex, treat as literal
            regex = re.compile(re.escape(pattern), regex_flags)
        
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                # Check if file matches pattern
                if not self._matches_pattern(file, file_pattern):
                    continue
                
                full_path = os.path.join(root, file)
                
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                except (IOError, OSError):
                    continue
                
                for i, line in enumerate(lines, 1):
                    if regex.search(line):
                        result = {
                            'file': full_path,
                            'line_num': i,
                            'line': line.rstrip(),
                            'context': []
                        }
                        
                        # Add context lines
                        if context_lines > 0:
                            start = max(0, i - context_lines - 1)
                            end = min(len(lines), i + context_lines)
                            result['context'] = [
                                (j, lines[j].rstrip()) 
                                for j in range(start, end)
                            ]
                        
                        results.append(result)
        
        return results
    
    def _matches_pattern(self, filename: str, file_pattern: str) -> bool:
        """Check if filename matches glob pattern"""
        import fnmatch
        return fnmatch.fnmatch(filename, file_pattern)
    
    def find_in_file(self, filepath: str, pattern: str) -> List[Tuple[int, str]]:
        """
        Search for pattern in a single file
        
        Args:
            filepath: Path to file to search
            pattern: Text pattern to search for
        
        Returns:
            List of (line_number, line) tuples
        """
        results = []
        regex_flags = 0 if self.case_sensitive else re.IGNORECASE
        
        try:
            regex = re.compile(pattern, regex_flags)
        except re.error:
            regex = re.compile(re.escape(pattern), regex_flags)
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f, 1):
                    if regex.search(line):
                        results.append((i, line.rstrip()))
        except (IOError, OSError):
            pass
        
        return results
    
    def find_and_replace(self, pattern: str, replacement: str, 
                       file_pattern: str = "*", dry_run: bool = True) -> dict:
        """
        Find and replace text (with safety check)
        
        Args:
            pattern: Text pattern to find
            replacement: Replacement text
            file_pattern: Glob pattern for files
            dry_run: If True, don't modify files, just report changes
        
        Returns:
            Dictionary with statistics
        """
        stats = {
            'files_matched': 0,
            'replacements': 0,
            'changes': []  # List of (filepath, count_changes)
        }
        
        try:
            regex = re.compile(pattern)
        except re.error:
            regex = re.compile(re.escape(pattern))
        
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                if not self._matches_pattern(file, file_pattern):
                    continue
                
                full_path = os.path.join(root, file)
                
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    new_content, count = regex.subn(replacement, content)
                    
                    if count > 0:
                        stats['files_matched'] += 1
                        stats['replacements'] += count
                        stats['changes'].append((full_path, count))
                        
                        if not dry_run:
                            with open(full_path, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                except (IOError, OSError):
                    pass
        
        return stats


def search_text(root_path: str, pattern: str, file_type: str = None,
               case_sensitive: bool = False) -> List[dict]:
    """
    Convenient function to search for text
    
    Args:
        root_path: Root directory to search
        pattern: Text pattern to search for
        file_type: File extension to search (e.g., "py", "md")
        case_sensitive: Case-sensitive search
    
    Returns:
        List of search results
    """
    searcher = TextSearcher(root_path, case_sensitive)
    
    if file_type:
        file_pattern = f"*.{file_type}"
    else:
        file_pattern = "*"
    
    return searcher.search(pattern, file_pattern)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python grep_search.py <path> <pattern> [--type ext] [--context N]")
        sys.exit(1)
    
    root = sys.argv[1]
    pattern = sys.argv[2]
    
    file_type = None
    context = 0
    
    # Parse options
    for i, arg in enumerate(sys.argv[3:]):
        if arg == "--type" and i + 3 < len(sys.argv):
            file_type = sys.argv[i + 4]
        elif arg == "--context" and i + 3 < len(sys.argv):
            context = int(sys.argv[i + 4])
    
    results = search_text(root, pattern, file_type)
    
    for result in results[:50]:  # Show first 50 results
        print(f"{result['file']}:{result['line_num']}: {result['line']}")
    
    if len(results) > 50:
        print(f"... and {len(results) - 50} more matches")
```

## Integration Example

```python
from grep_search import TextSearcher

searcher = TextSearcher("/home/user/project")

# Basic search
results = searcher.search("TODO", file_pattern="*.py")

# With context
results = searcher.search("def calculate", file_pattern="*.py", context_lines=2)

# Find and replace (dry run)
stats = searcher.find_and_replace("old_name", "new_name", file_pattern="*.py", dry_run=True)

# For single file
lines = searcher.find_in_file("path/to/file.py", "function_name")
```
