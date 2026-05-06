import subprocess
import json
import os
from dotenv import load_dotenv

load_dotenv()


class MCPClient:
    def __init__(self):
        self.proc = None

    def start(self):
        cmd = [
            "docker", "run", "-i", "--rm",
            "-e", f"GITHUB_PERSONAL_ACCESS_TOKEN={os.getenv('GITHUB_TOKEN')}",
            "ghcr.io/github/github-mcp-server"
        ]

        self.proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

    def send(self, req):
        self.proc.stdin.write(json.dumps(req) + "\n")
        self.proc.stdin.flush()

    def recv(self):
        while True:
            line = self.proc.stdout.readline()
            if not line:
                raise RuntimeError("MCP died")

            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue

    def initialize(self):
        # 1. initialize
        self.send({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test", "version": "1.0"}
            }
        })
        self.recv()

        # 2. initialized
        self.send({
            "jsonrpc": "2.0",
            "method": "initialized",
            "params": {}
        })

    def list_tools(self):
        self.send({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        })
        return self.recv()

    def call_tool(self, name, arguments, req_id=3):
        self.send({
            "jsonrpc": "2.0",
            "id": req_id,
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments
            }
        })
        return self.recv()

    def close(self):
        if self.proc:
            self.proc.kill()


if __name__ == "__main__":
    client = MCPClient()
    client.start()
    client.initialize()

    # ===== 1. List tools =====
    tools_res = client.list_tools()
    tools = tools_res["result"]["tools"]

    print("=== TOOLS ===")
    for t in tools:
        print("-", t["name"])

    # ===== 2. Call list_branches =====
    print("\n=== CALL list_branches ===")

    res = client.call_tool(
        "list_branches",
        {
            "owner": "github",
            "repo": "github-mcp-server"
        }
    )

    # MCP trả về dạng text → cần parse lại
    try:
        content = res["result"]["content"][0]["text"]
        branches = json.loads(content)

        print(f"Found {len(branches)} branches:")
        for b in branches[:5]:
            print("-", b["name"])

    except Exception as e:
        print("Raw response:")
        print(json.dumps(res, indent=2))

    client.close()