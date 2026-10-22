
import asyncio
import sys
from pathlib import Path

import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


MODEL = "qwen2.5:3b"
SERVER_PATH = Path(__file__).with_name("server.py")

SYSTEM_PROMPT = """
You are a safe AI DevOps assistant.
Use available MCP tools when they are relevant to the user's request.
Explain tool results in simple English.
Never claim a tool was executed unless it actually ran.
Do not suggest destructive actions as automatic fixes.
"""


async def main():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
    )

    print("Starting AI DevOps Agent...")
    print(f"Model: {MODEL}")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Discover available MCP tools
            tool_result = await session.list_tools()
            mcp_tools = tool_result.tools

            print("\nConnected to MCP server.")
            print("Available tools:")

            for tool in mcp_tools:
                print(f"- {tool.name}: {tool.description}")

            # Convert MCP tool definitions to Ollama tool schemas
            ollama_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or tool.name,
                        "parameters": tool.input_schema,
                    },
                }
                for tool in mcp_tools
            ]

            messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                }
            ]

            print("\nAI DevOps Agent is ready.")
            print("Try: List my Docker containers")
            print("Type 'exit' to quit.\n")

            while True:
                try:
                    user_input = input("You: ").strip()
                except (EOFError, KeyboardInterrupt):
                    print("\nAgent stopped.")
                    break

                if user_input.lower() in {"exit", "quit"}:
                    print("Agent stopped.")
                    break

                if not user_input:
                    continue

                messages.append({
                    "role": "user",
                    "content": user_input,
                })

                try:
                    # Limit the number of tool-call rounds
                    for _ in range(4):
                        response = ollama.chat(
                            model=MODEL,
                            messages=messages,
                            tools=ollama_tools,
                        )

                        assistant_message = response.message
                        messages.append(assistant_message)

                        tool_calls = assistant_message.tool_calls or []

                        if not tool_calls:
                            print(f"\nAI: {assistant_message.content}\n")
                            break

                        for call in tool_calls:
                            name = call.function.name
                            arguments = call.function.arguments

                            # Only permit tools discovered from this MCP server
                            allowed_tools = {
                                tool.name: tool for tool in mcp_tools
                            }

                            if name not in allowed_tools:
                                result_text = f"Rejected unknown tool: {name}"
                            else:
                                try:
                                    print(f"\nCalling MCP tool: {name}")
                                    print(f"Arguments: {arguments}")

                                    result = await session.call_tool(
                                        name,
                                        arguments=arguments,
                                    )

                                    result_text = "\n".join(
                                        item.text
                                        for item in result.content
                                        if hasattr(item, "text")
                                    )

                                    if result.isError:
                                        result_text = (
                                            "Tool reported an error: "
                                            + result_text
                                        )

                                except Exception as error:
                                    result_text = (
                                        f"Tool execution failed: {error}"
                                    )

                            print(f"Tool result: {result_text}")

                            messages.append({
                                "role": "tool",
                                "tool_name": name,
                                "content": result_text,
                            })

                    else:
                        print(
                            "\nAgent stopped after reaching the "
                            "tool-call limit. Try a simpler request.\n"
                        )

                except Exception as error:
                    print(f"\nAgent error: {error}\n")


if __name__ == "__main__":
    asyncio.run(main())

