
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_path = Path(__file__).with_name("server.py")

    params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)],
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 1. Discover resources
            print("\n=== RESOURCES ===")
            resources = await session.list_resources()

            for resource in resources.resources:
                print("Name:", resource.name)
                print("URI:", resource.uri)

            # 2. Read the Docker guide
            print("\n=== READ RESOURCE ===")
            result = await session.read_resource(
                "devops://docker-guide"
            )

            for item in result.contents:
                if hasattr(item, "text"):
                    print(item.text)

            # 3. Discover prompts
            print("\n=== PROMPTS ===")
            prompts = await session.list_prompts()

            for prompt in prompts.prompts:
                print("-", prompt.name)

            # 4. Get the Docker error prompt
            print("\n=== DOCKER ERROR PROMPT ===")
            result = await session.get_prompt(
                "explain_docker_error",
                arguments={
                    "error_message": "Cannot connect to Docker daemon"
                },
            )

            for message in result.messages:
                print(message.content.text)

            # 5. Get the learning-plan prompt
            print("\n=== LEARNING PLAN PROMPT ===")
            result = await session.get_prompt(
                "devops_learning_plan",
                arguments={
                    "topic": "Kubernetes",
                    "level": "beginner",
                },
            )

            for message in result.messages:
                print(message.content.text)


if __name__ == "__main__":
    asyncio.run(main())

