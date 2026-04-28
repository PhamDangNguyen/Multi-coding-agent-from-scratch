import asyncio
import json
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession

async def main():
    """Connect to MCP weather server and test tools."""
    server_params = StdioServerParameters(
        command="python",
        args=["mcp/weather.py"],
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as client:
            print("🔌 Initializing MCP client...")
            await client.initialize()
            print("✅ Connected successfully!\n")

            # ========== STEP 1: List all available tools ==========
            print("=" * 50)
            print("📋 Available Tools:")
            print("=" * 50)
            tools_response = await client.list_tools()
            tools = tools_response.tools if hasattr(tools_response, 'tools') else tools_response
            
            print(f"\n📊 Total tools: {len(tools)}\n")
            
            for i, tool in enumerate(tools, 1):
                tool_name = tool.name if hasattr(tool, 'name') else tool[0]
                tool_desc = tool.description if hasattr(tool, 'description') else (tool[1] if len(tool) > 1 else "No description")
                tool_schema = tool.inputSchema if hasattr(tool, 'inputSchema') else (tool[2] if len(tool) > 2 else {})
                
                print(f"{i}. {tool_name}")
                print(f"   Description: {tool_desc}")
                if tool_schema:
                    print(f"   Parameters: {json.dumps(tool_schema, indent=2)}")
                print()

            # ========== STEP 2: Test Tool 1 - get_forecast ==========
            print("=" * 50)
            print("🌦️  Test Tool 1: get_forecast")
            print("=" * 50)
            print("📍 Getting forecast for San Francisco (37.7749, -122.4194)...\n")
            
            result1 = await client.call_tool(
                "get_forecast",
                {"latitude": 37.7749, "longitude": -122.4194}
            )
            print("Result:")
            print(result1.content[0].text)

            print("\n")

            # ========== STEP 3: Test Tool 2 - get_alerts ==========
            print("=" * 50)
            print("⚠️  Test Tool 2: get_alerts")
            print("=" * 50)
            print("📍 Getting alerts for California (CA)...\n")
            
            result2 = await client.call_tool(
                "get_alerts",
                {"state": "CA"}
            )
            print("Result:")
            print(result2.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())