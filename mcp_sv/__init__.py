"""mcp_sv package initializer.

Expose a helper to run the MCP tool adapter. Importing this package
must not start the server automatically (so tests can import safely).
"""

from pathlib import Path
from typing import Optional


def run_server(root: Optional[Path] = None) -> None:
	"""Create the tool registry, mount tools and run the MCP adapter.

	If `root` is provided, it will be added to sys.path so local modules
	(like `tools`) can be imported when running as a subprocess.
	"""
	import sys
	from pathlib import Path as _Path

	if root is None:
		root = _Path(__file__).resolve().parents[1]

	# Ensure project root is on sys.path when running as a subprocess
	root = _Path(root)
	if str(root) not in sys.path:
		sys.path.append(str(root))

	from tools.registry import ToolRegistry
	from mcp_sv.mcp_server import MCPToolAdapter
	from tools.bash.read_file import ReadFileTool

	registry = ToolRegistry()
	registry.register(ReadFileTool())

	adapter = MCPToolAdapter(registry)
	adapter.run()


__all__ = ["run_server"]