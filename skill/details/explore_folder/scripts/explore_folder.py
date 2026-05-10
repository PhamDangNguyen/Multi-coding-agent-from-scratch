from pathlib import Path
from typing import Dict, Optional
import os


class ExplorerToolkit:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
    
    def get_directory_info(self) -> Dict:
        return {
            'path': str(self.root_path),
            'exists': self.root_path.exists(),
            'is_dir': self.root_path.is_dir(),
            'children': self._count_children(),
            'statistics': self._get_statistics(),
        }
    
    def _count_children(self) -> Dict[str, int]:
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
        stats['largest_files'] = sorted(all_files, key=lambda x: x[1], reverse=True)[:5]
        return stats


def explore_folder(path: str) -> Dict:
    explorer = ExplorerToolkit(path)
    return explorer.get_directory_info()
