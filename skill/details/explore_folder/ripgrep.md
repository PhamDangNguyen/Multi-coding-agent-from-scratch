# Ripgrep (rg) Advanced Usage

## What is Ripgrep?

Ripgrep is a line-oriented search tool that recursively searches your current directory for a regex pattern. It's dramatically faster than grep and has sensible defaults.

## Installation

```bash
# macOS
brew install ripgrep

# Ubuntu/Debian
sudo apt install ripgrep

# Fedora
sudo dnf install ripgrep

# Alpine
apk add ripgrep

# Or from source
cargo install ripgrep
```

## Basic Usage

```bash
# Simple search
rg "pattern" /path/to/search

# Case-insensitive
rg -i "pattern" /path/to/search

# Search for whole word
rg -w "word" /path/to/search

# Show line numbers
rg -n "pattern" /path/to/search

# Show filename only
rg -l "pattern" /path/to/search

# Count matches
rg -c "pattern" /path/to/search
```

## Advanced Usage

### Context Lines

```bash
# Show 3 lines before and after
rg -A 3 -B 3 "pattern" /path/to/search

# Show 2 lines after
rg -A 2 "pattern" /path/to/search

# Show 2 lines before
rg -B 2 "pattern" /path/to/search
```

### File Type Filtering

```bash
# Search only Python files
rg -t py "pattern" /path/to/search

# Search only JavaScript files
rg -t js "pattern" /path/to/search

# List available file types
rg --type-list
```

### Ignore Patterns

```bash
# Ignore directories
rg --glob "!.git" "pattern" /path/to/search

# Ignore multiple patterns
rg --glob "!node_modules" --glob "!*.pyc" "pattern" .

# Use custom ignore file
rg --ignore-file my_ignore "pattern" /path/to/search
```

### Regular Expression Features

```bash
# Word boundary
rg -w "function" /path/to/search

# OR pattern
rg "(error|warning|info)" /path/to/search

# Beginning of line
rg "^import" /path/to/search

# End of line
rg "\.py$" /path/to/search

# Capture groups (with color)
rg "(\w+)@(\w+)" /path/to/search
```

### Replace Mode

```bash
# Preview replacements (dry run)
rg "old_pattern" --replace "new_pattern" /path/to/search

# Show replaced text in context
rg "old_pattern" --replace "new_pattern" -C 2 /path/to/search
```

## Python Integration

### ripgrep.py

```python
"""
Ripgrep integration - Fast text search using ripgrep
"""

import subprocess
from typing import List, Optional, Tuple
from pathlib import Path


class RipgrepSearcher:
    """Interface to ripgrep for fast searching"""
    
    def __init__(self, root_path: str):
        """Initialize ripgrep searcher"""
        self.root_path = Path(root_path)
    
    def search(self, pattern: str, file_type: Optional[str] = None,
              context_after: int = 0, context_before: int = 0,
              case_insensitive: bool = False) -> List[dict]:
        """
        Search using ripgrep
        
        Args:
            pattern: Regex pattern to search
            file_type: File type filter (e.g., "py" for Python)
            context_after: Lines after match
            context_before: Lines before match
            case_insensitive: Case-insensitive search
        
        Returns:
            List of match dictionaries
        """
        cmd = ["rg", "--json"]
        
        if file_type:
            cmd.extend(["-t", file_type])
        
        if context_after:
            cmd.extend(["-A", str(context_after)])
        
        if context_before:
            cmd.extend(["-B", str(context_before)])
        
        if case_insensitive:
            cmd.append("-i")
        
        cmd.extend([pattern, str(self.root_path)])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return self._parse_json_output(result.stdout)
        except FileNotFoundError:
            print("ripgrep (rg) not found. Install with: cargo install ripgrep")
            return []
    
    def _parse_json_output(self, output: str) -> List[dict]:
        """Parse JSON output from ripgrep"""
        import json
        
        results = []
        for line in output.strip().split('\n'):
            if line:
                try:
                    results.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        
        return results
    
    def search_simple(self, pattern: str, file_type: Optional[str] = None) -> List[str]:
        """Simple search returning just matching lines"""
        cmd = ["rg", "-n"]
        
        if file_type:
            cmd.extend(["-t", file_type])
        
        cmd.extend([pattern, str(self.root_path)])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.stdout.strip().split('\n') if result.stdout else []
        except FileNotFoundError:
            return []


def search_fast(root_path: str, pattern: str, file_type: Optional[str] = None) -> List[str]:
    """Quick search function"""
    searcher = RipgrepSearcher(root_path)
    return searcher.search_simple(pattern, file_type)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python ripgrep.py <path> <pattern> [--type ext]")
        sys.exit(1)
    
    root = sys.argv[1]
    pattern = sys.argv[2]
    file_type = None
    
    if "--type" in sys.argv:
        file_type = sys.argv[sys.argv.index("--type") + 1]
    
    results = search_fast(root, pattern, file_type)
    for result in results[:50]:
        print(result)
    
    if len(results) > 50:
        print(f"... and {len(results) - 50} more")
```

## Performance Comparison

| Tool | Speed | Features | Memory |
|------|-------|----------|--------|
| grep | Slow | Basic | Low |
| ack | Medium | Good | Medium |
| ripgrep | Very Fast | Excellent | Low |

Ripgrep is typically 5-100x faster than standard grep!

## Tips & Tricks

1. **Use .ignore files**: Create `.ignore` file in project root with patterns to ignore
2. **Combine with sorting**: `rg "pattern" | sort`
3. **Find and highlight**: `rg -A 2 -B 2 "error"`
4. **Generate reports**: `rg "TODO" -t py > todo_list.txt`
5. **Stats mode**: `rg --stats "pattern"` for detailed statistics

## Common Use Cases

### Find all TODOs
```bash
rg "TODO|FIXME" -t py .
```

### Find long functions
```bash
rg -n "^def " src/
```

### Search specific file types
```bash
rg -t py -t js "error" .
```

### Most recent occurrences
```bash
git log -S "pattern" --oneline
```

## Alternatives

- **ag** (The Silver Searcher): Similar to ripgrep but slightly slower
- **ack**: Good for code search but slower than ripgrep
- **grep**: Standard Unix tool, but simple and slow for large codebases
