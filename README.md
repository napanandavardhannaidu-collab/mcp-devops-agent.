# AI-Powered DevOps Agent using MCP and Ollama

## Overview

A learning project that connects a local Large Language Model (LLM) to DevOps tools using the Model Context Protocol (MCP).

The agent accepts natural-language requests, selects an available tool through Ollama's tool-calling interface, executes that tool through an MCP client, and uses the result to generate a response.

## Features

- Local LLM integration with Ollama (`qwen2.5:3b`)
- MCP server exposing DevOps tools
- Docker container inspection
- DevOps tips for Docker, Kubernetes, Linux, and Git
- MCP resources and reusable prompts
- Input validation and basic error handling
- MCP Inspector exploration and testing

## Architecture

User request → Ollama LLM → Tool selection → MCP client → MCP server → Tool result → LLM response

## Tech Stack

- Python
- Ollama
- Model Context Protocol (MCP)
- Docker SDK for Python
- Ubuntu / WSL
- MCP Inspector

## Prerequisites

- Python 3.12 or a compatible version
- Docker Engine accessible from your environment
- Ollama installed
- The `qwen2.5:3b` model downloaded

## Setup

Clone the repository, then run:

```bash
cd mcp-devops-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ollama pull qwen2.5:3b
```

Ensure Docker and Ollama are running and accessible.

## Run the Agent

```bash
python agent.py
```

Example request:

```text
List my Docker containers
```

Type `exit` to stop the agent.

## Safety Notes

The Docker inspection tool is intended to be read-only. Review any future tools carefully before allowing them to change infrastructure. Never commit API keys, passwords, access tokens, or private configuration files.

## Project Status

Learning prototype. Further work includes stronger argument validation, improved testing, and expanded DevOps diagnostics.

## Learning Outcomes

- Building an MCP server and client
- Exposing tools, resources, and prompts
- Connecting an LLM to external tools
- Testing local AI integrations
- Practising safe DevOps automation

## License

Choose a license before distributing or reusing the project.
