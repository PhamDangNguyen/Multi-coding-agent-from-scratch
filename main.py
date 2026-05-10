from pathlib import Path
from mcp_sv import run_server


if __name__ == "__main__":
	# Run the MCP tool adapter server (adds project root to sys.path internally)
	run_server()
