import subprocess
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_mcp_list_tools():
    cmd = [
        "docker", "run", "-i", "--rm",
        "-e", f"GITHUB_PERSONAL_ACCESS_TOKEN={os.getenv('GITHUB_TOKEN')}",
        "ghcr.io/github/github-mcp-server"
    ]

    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    def send(req):
        proc.stdin.write(json.dumps(req) + "\n")
        proc.stdin.flush()

    def recv():
        while True:
            line = proc.stdout.readline()
            if not line:
                raise RuntimeError("MCP died")
            try:
                return json.loads(line)
            except:
                continue

    # 1. initialize
    send({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0"}
        }
    })
    recv()  # bỏ qua init response

    # 2. initialized
    send({
        "jsonrpc": "2.0",
        "method": "initialized",
        "params": {}
    })

    # 3. tools/list
    send({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list"
    })

    res = recv()
    return res


if __name__ == "__main__":
    res = test_mcp_list_tools()
    tools = res["result"]["tools"]

    simple_tools = [
        {
            "name": t["name"],
            "description": t.get("description"),
            "params": t.get("inputSchema", {}).get("properties", {})
        }
        for t in tools
    ]

    print(json.dumps(simple_tools, indent=2))