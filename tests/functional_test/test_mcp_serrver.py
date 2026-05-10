# client.py

import asyncio

from mcp import ClientSession
from mcp.client.stdio import stdio_client
from mcp.client.stdio import StdioServerParameters


async def main():

    server_params = StdioServerParameters(
        command="python",
        args=["main.py"]
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            # init MCP connection
            await session.initialize()

            # list available tools
            tools = await session.list_tools()

            print("TOOLS:")
            print(tools)

            # call tool
            result = await session.call_tool(
                "read_file",
                {
                    "path": "/home/dangnguyen/Side_project/Multi-agent-from-scratch/README.md"
                }
            )

            # print(result)

if __name__ == "__main__":
    asyncio.run(main()) 