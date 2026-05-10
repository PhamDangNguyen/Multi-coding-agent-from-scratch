from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]  
sys.path.append(str(ROOT))
from mcp_sv import run_server
if __name__ == "__main__":
    run_server()