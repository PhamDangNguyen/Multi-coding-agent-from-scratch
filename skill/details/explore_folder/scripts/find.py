import os
from pathlib import Path
from typing import Optional, List
from datetime import datetime, timedelta
import fnmatch


class FileFinder:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
    
    def find_by_name(self, pattern: str, exclude_hidden: bool = False) -> List[str]:
        matches = []
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                if exclude_hidden and file.startswith("."):
                    continue
                if fnmatch.fnmatch(file, pattern):
                    matches.append(os.path.join(root, file))
        return sorted(matches)
    
    def find_by_extension(self, *extensions: str) -> List[str]:
        matches = []
        exts = [f".{ext}" if not ext.startswith(".") else ext for ext in extensions]
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                if Path(file).suffix in exts:
                    matches.append(os.path.join(root, file))
        return sorted(matches)
    
    def find_by_size(self, min_size: int = None, max_size: int = None) -> List[tuple]:
        matches = []
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    size = os.path.getsize(filepath)
                    if min_size and size < min_size:
                        continue
                    if max_size and size > max_size:
                        continue
                    matches.append((filepath, size))
                except OSError:
                    pass
        return sorted(matches, key=lambda x: x[1], reverse=True)
    
    def find_by_date(self, days: int = None) -> List[tuple]:
        matches = []
        if days:
            cutoff = datetime.now() - timedelta(days=days)
            cutoff_timestamp = cutoff.timestamp()
            for root, dirs, files in os.walk(self.root_path):
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        mtime = os.path.getmtime(filepath)
                        if mtime >= cutoff_timestamp:
                            matches.append((filepath, datetime.fromtimestamp(mtime)))
                    except OSError:
                        pass
        return sorted(matches, key=lambda x: x[1], reverse=True)


def find_files(root_path: str, pattern: str = None, extension: str = None) -> List[str]:
    finder = FileFinder(root_path)
    if extension:
        return finder.find_by_extension(extension)
    elif pattern:
        return finder.find_by_name(pattern)
    return []
