# core/mcp_adapter.py

from mcp.server.fastmcp import FastMCP


class MCPToolAdapter:

    def __init__(self, registry):
        self.registry = registry
        self.mcp = FastMCP("agent-system")

    def mount_tools(self):

        for tool in self.registry.tools.values():

            self.mcp.tool(
                name=tool.name,
                description=tool.description,
                title=tool.title
            )(tool.execute)

    def run(self):

        self.mount_tools()

        self.mcp.run()