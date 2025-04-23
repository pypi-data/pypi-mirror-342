# baml‑agents

<a href="https://discord.gg/hCppPqm6"><img alt="Discord" src="https://img.shields.io/discord/1119368998161752075?logo=discord&logoColor=white&style=flat"></a>
[![License: MIT](https://img.shields.io/badge/license-MIT-success.svg)](https://opensource.org/licenses/MIT)
<a href="https://badge.fury.io/py/baml-agents"><img src="https://badge.fury.io/py/baml-agents.svg" alt="PyPI version" /></a>
[![status-prototype](https://img.shields.io/badge/status-prototype-yellow.svg)](https://github.com/mkenney/software-guides/blob/master/STABILITY-BADGES.md#experimental)
<a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>

**Building Agents with [BAML](https://www.boundaryml.com/) for structured generation with LLMs, [MCP Tools](https://modelcontextprotocol.io/docs/concepts/tools), and [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) principles**

This repository shares useful patterns I use when working with BAML. The API is unstable and may change in future versions. We recommend installing a specific version:

```bash
pip install baml‑agents==0.6.0
```

Feedback is always welcome!

## Contents

1.  [Flexible LLM Client Management in BAML](notebooks/01_llm_clients.ipynb)
    - Effortlessly switch between different LLM providers (like OpenAI, Anthropic, Google) at runtime using simple helper functions.
    - Bridge compatibility gaps: Connect to unsupported LLM backends or tracing systems (e.g., Langfuse, LangSmith) via standard proxy setups.
    - Solve common configuration issues: Learn alternatives for managing API keys and client settings if environment variables aren't suitable.
2.  [Introduction to AI Tool Use with BAML](notebooks/02_intro_to_ai_using_tools.ipynb)
    - Learn how to define custom actions (tools) for your AI using Pydantic models, making your agents capable of _doing_ things.
    - See how to integrate these tools with BAML manually or dynamically using `ActionRunner` for flexible structured outputs.
    - Understand how BAML translates goals into structured LLM calls that select and utilize the appropriate tool.
3.  [Integrating Standardized MCP Tools with BAML](notebooks/03_using_mcp_tools_with_baml.ipynb)
    - Discover how to leverage the Model Context Protocol (MCP) to easily plug-and-play pre-built 3rd party tools (like calculators, web search) into your BAML agents.
    - See `ActionRunner` in action, automatically discovering and integrating tools from MCP servers with minimal configuration.
    - Learn techniques to filter and select specific MCP tools to offer to the LLM, controlling the agent's capabilities precisely.

## Running the Notebooks

To run code from the `notebooks/` folder, you'll first need to:

- Install the [`uv` python package manager](https://docs.astral.sh/uv/).
- Install all dependencies: `uv sync --dev`
- Generates necessary BAML code: `uv run baml-cli generate`
  - Alternatively, you can use the [VSCode extension](https://marketplace.visualstudio.com/items?itemName=Boundary.baml-extension) to do it automatically every time you edit a `.baml` file.
