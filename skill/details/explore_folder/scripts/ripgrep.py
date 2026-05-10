import subprocess
from pathlib import Path
from typing import Optional, List
import json


class RipgrepSearcher:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
    
    def search(self, pattern: str, file_type: Optional[str] = None) -> List[str]:
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
    searcher = RipgrepSearcher(root_path)
    return searcher.search(pattern, file_type)
