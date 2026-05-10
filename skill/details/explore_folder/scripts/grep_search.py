import re
from pathlib import Path
from typing import Optional, List
import fnmatch


class TextSearcher:
    def __init__(self, root_path: str, case_sensitive: bool = False):
        self.root_path = Path(root_path)
        self.case_sensitive = case_sensitive
    
    def search(self, pattern: str, file_pattern: str = "*", context_lines: int = 0) -> List[dict]:
        results = []
        regex_flags = 0 if self.case_sensitive else re.IGNORECASE
        
        try:
            regex = re.compile(pattern, regex_flags)
        except re.error:
            regex = re.compile(re.escape(pattern), regex_flags)
        
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                if not fnmatch.fnmatch(file, file_pattern):
                    continue
                
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                except (IOError, OSError):
                    continue
                
                for i, line in enumerate(lines, 1):
                    if regex.search(line):
                        results.append({
                            'file': filepath,
                            'line_num': i,
                            'line': line.rstrip()
                        })
        
        return results


def search_text(root_path: str, pattern: str, file_type: str = None) -> List[dict]:
    searcher = TextSearcher(root_path)
    if file_type:
        file_pattern = f"*.{file_type}"
    else:
        file_pattern = "*"
    return searcher.search(pattern, file_pattern)
