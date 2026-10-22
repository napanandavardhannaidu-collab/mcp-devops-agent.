
import docker
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("DevOps Learning Server")


# TOOL 1: Add two numbers
@mcp.tool()
def add_numbers(a: int, b: int) -> str:
    """Add two integers."""

    if isinstance(a, bool) or not isinstance(a, int):
        return "Error: a must be an integer."

    if isinstance(b, bool) or not isinstance(b, int):
        return "Error: b must be an integer."

    return str(a + b)


# TOOL 2: Return a DevOps tip
@mcp.tool()
def get_devops_tip(topic: str) -> str:
    """Return a tip about Docker, Kubernetes, Linux, or Git."""

    if not isinstance(topic, str) or not topic.strip():
        return "Error: topic cannot be empty."

    tips = {
        "docker": "Use trusted, small base images.",
        "kubernetes": "Use readiness probes to check application readiness.",
        "linux": "Use top, free -h, and df -h to inspect system resources.",
        "git": "Make small, meaningful commits.",
    }

    topic = topic.strip().lower()

    for key, tip in tips.items():
        if key in topic:
            return tip

    return "Unsupported topic. Choose Docker, Kubernetes, Linux, or Git."


# TOOL 3: Inspect Docker containers
@mcp.tool()
def list_docker_containers() -> str:
    """List running and stopped Docker containers."""

    client = None

    try:
        client = docker.from_env(timeout=5)
        client.ping()
        containers = client.containers.list(all=True)

        if not containers:
            return "No Docker containers found."

        return "\n".join(
            f"Name: {c.name}, Status: {c.status}, Image: {c.image.tags}"
            for c in containers
        )

    except docker.errors.DockerException as error:
        return f"Docker connection failed: {error}"

    except Exception as error:
        return f"Unexpected error: {error}"

    finally:
        if client is not None:
            client.close()


# RESOURCE: Read-only DevOps guide
@mcp.resource("devops://docker-guide")
def docker_guide() -> str:
    """Provide a short Docker troubleshooting guide."""

    return """
Docker Troubleshooting Guide

1. Check Docker availability: docker version
2. List running containers: docker ps
3. List all containers: docker ps -a
4. Inspect container logs: docker logs CONTAINER_NAME
5. Inspect container details: docker inspect CONTAINER_NAME

Safety:
- Inspect before changing anything.
- Do not expose passwords or API keys in logs.
- Do not delete containers unless you understand the impact.
"""


# PROMPT 1: Explain a Docker error
@mcp.prompt()
def explain_docker_error(error_message: str) -> str:
    """Create a prompt for troubleshooting a Docker error."""

    return f"""
You are a helpful DevOps tutor.

Explain this Docker error in simple English:

{error_message}

Provide:
1. What the error means
2. Likely causes
3. Safe diagnostic commands
4. Possible solutions
Do not suggest destructive commands without explaining their risks.
"""


# PROMPT 2: Create a learning plan
@mcp.prompt()
def devops_learning_plan(topic: str, level: str = "beginner") -> str:
    """Create a reusable DevOps learning-plan prompt."""

    return f"""
Act as a DevOps tutor.

Topic: {topic}
Learner level: {level}

Create a practical learning plan with:
1. Simple concepts
2. Commands to practise
3. A small hands-on exercise
4. A test to check understanding
"""


if __name__ == "__main__":
    mcp.run(transport="stdio")
