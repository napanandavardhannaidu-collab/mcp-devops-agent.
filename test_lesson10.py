
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_path = Path(__file__).with_name("server.py")

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()

            print("Connected to MCP server!")
            print("\nAvailable tools:")

            for tool in tools.tools:
                print(f"- {tool.name}")

            # Test 1: Valid addition
            print("\nTEST 1: Valid addition")
            result = await session.call_tool(
                "add_numbers",
                arguments={"a": 10, "b": 20},
            )
            for item in result.content:
                if hasattr(item, "text"):
                    print(item.text)

            # Test 2: Valid DevOps topic
            print("\nTEST 2: Valid topic")
            result = await session.call_tool(
                "get_devops_tip",
                arguments={"topic": "Docker"},
            )
            for item in result.content:
                if hasattr(item, "text"):
                    print(item.text)

            # Test 3: Empty topic
            print("\nTEST 3: Empty topic validation")
            result = await session.call_tool(
                "get_devops_tip",
                arguments={"topic": ""},
            )
            for item in result.content:
                if hasattr(item, "text"):
                    print(item.text)

            # Test 4: Unsupported topic
            print("\nTEST 4: Unsupported topic validation")
            result = await session.call_tool(
                "get_devops_tip",
                arguments={"topic": "Astrology"},
            )
            for item in result.content:
                if hasattr(item, "text"):
                    print(item.text)

            # Test 5: Docker inspection
            print("\nTEST 5: Docker inspection")
            result = await session.call_tool(
                "list_docker_containers",
                arguments={},
            )
            for item in result.content:
                if hasattr(item, "text"):
                    print(item.text)


if __name__ == "__main__":
    asyncio.run(main())
