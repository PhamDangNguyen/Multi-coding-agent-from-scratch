# Explore Folder - Advanced Reference

## Advanced Tree Generation

### Custom Tree Output

```python
from pathlib import Path

def pretty_tree(path: str, prefix: str = "", ignore: set = None) -> str:
    """Generate a pretty tree of directories"""
    
    if ignore is None:
        ignore = {'.git', '__pycache__', '.venv', '.env'}
    
    path_obj = Path(path)
    if not path_obj.exists():
        return f"Path not found: {path}"
    
    tree = f"{path_obj.name}/\n"
    
    def _tree(current_path: Path, prefix: str = ""):
        contents = sorted(current_path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
        contents = [x for x in contents if x.name not in ignore]
        
        for i, path_obj in enumerate(contents):
            is_last = i == len(contents) - 1
            current_prefix = "└── " if is_last else "├── "
            tree_prefix = "    " if is_last else "│   "
            
            tree_str = f"{prefix}{current_prefix}{path_obj.name}"
            if path_obj.is_dir():
                tree_str += "/"
            tree.add_line(tree_str)
            
            if path_obj.is_dir() and path_obj.name not in ignore:
                _tree(path_obj, prefix + tree_prefix)
    
    _tree(path_obj)
    return tree
```

## Advanced Search Recipes

### Find files by multiple criteria

```bash
# Find Python files modified in last 24 hours
find . -name "*.py" -mtime -1

# Find files larger than 10MB modified this week
find . -size +10M -mtime -7

# Find empty files
find . -type f -empty

# Find files with specific permissions
find . -type f -perm 644
```

### Complex grep/ripgrep patterns

```bash
# Search for lines with word boundaries
rg -w "function" src/

# Search excluding multiple patterns
rg --glob "!*.pyc" --glob "!*.log" "error" .

# Show only matches without filename
rg -o "pattern" src/

# Show statistics
rg --stats "pattern" src/

# Search and replace (use with caution!)
rg --replace "replacement" "pattern" src/
```

## Integration with Git

### Find changes across commits

```bash
# Show files changed between commits
git diff --name-status COMMIT1 COMMIT2

# Find who last modified a file
git log --oneline -n 5 -- path/to/file

# Find files that changed since a tag
git diff --name-status TAG..HEAD

# Show recent changes per file
git log --pretty=format:"%h %s" -- path/to/file | head -5
```

## Performance Optimization

### For Large Codebases

#### Use ripgrep instead of grep
```bash
# Ripgrep is typically 10-100x faster
-Replace: grep -r "pattern" .
+With:    rg "pattern" .
```

#### Exclude unnecessary directories
```bash
# Speed up searches significantly
find . -path ./node_modules -prune -o -name "*.js" -type f -print
rg --glob "!node_modules" --glob "!.git" "pattern" .
```

#### Use fd instead of find
```bash
# fd is faster and has simpler syntax than find
fd "pattern" /path/to/folder
fd -e py /path/to/folder  # By extension
```

## Statistics & Analysis

### Code Statistics

```bash
# Count lines of code by file type
find . -name "*.py" -type f -exec wc -l {} \; | awk '{sum+=$1} END {print sum}'

# Show file count by extension
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn

# Disk usage by directory
du -sh */
```

### Project Health Analysis

```bash
# Find TODO/FIXME comments
rg -i "TODO|FIXME" src/ --color=never

# Find long functions (more than 100 lines)
# (Implementation depends on language)

# Find unused variables (varies by language)
# Use language-specific linters
```

## Practical Workflows

### 1. Project Onboarding

```bash
# Get overview of project structure
tree -L 2 -I 'node_modules|.git|__pycache__'

# Count files by type
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn

# Find entry points
find . -name "main.*" -o -name "index.*" -o -name "app.*"

# Check documentation
find . -name "README*" -o -name "*.md"
```

### 2. Code Review

```bash
# Find recent changes
git diff HEAD~10..HEAD --name-only

# Show what changed in specific files
git diff HEAD~10 -- path/to/file

# Find complex functions
rg -n "def|class" src/ | head -20
```

### 3. Debugging

```bash
# Find all instances of error handling
rg -i "exception|error|try|catch" src/

# Find specific error messages
rg "Error: database" .

# Trace function calls
rg "my_function\(" src/ -n -B 1 -A 1
```

### 4. Refactoring

```bash
# Find all imports of a module
rg "from old_module|import old_module" .

# Find all usages of a function
rg "function_name\(" src/ -n

# Show duplicated code patterns
rg -A 5 "similar_pattern" src/
```

## Shell Functions for Common Tasks

Add these to your `.bashrc` or `.zshrc`:

```bash
# Count total lines of code
cloc() {
    find . -type f -name "*.${1:-py}" -exec wc -l {} + | tail -1
}

# Find and display file
ff() {
    find . -name "*$1*" -type f
}

# Search recursively
ss() {
    rg -i "$1" .
}

# Show tree with depth limit
tr() {
    tree -L ${2:-2} -I 'node_modules|.git|__pycache__|.venv' $1
}

# Find large files
large() {
    find . -type f -size +${1:-100}M -exec ls -lh {} \;
}
```

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Search is slow | Use `rg` instead of `grep`, exclude large directories |
| Too many results | Use `--glob` to exclude patterns, limit file types with `-t` |
| Permission denied | Use `2>/dev/null` to suppress errors, or run with appropriate permissions |
| Large output | Pipe to `less`, save to file, or limit with `head` |
| Special characters in search | Escape or use `--literal` flag, use `--` to end flags |

## Further Reading

- `man find` - Complete find documentation
- `man grep` - Complete grep documentation
- `rg --help` - Ripgrep help and options
- `man tree` - Tree documentation
- `man git-ls-files` - Git ls-files documentation
