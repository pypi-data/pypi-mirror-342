# baml‑agents

`pip install baml-agents`

An example repo demonstrating how to build agentic LLM systems with BAML and plug‑and‑play MCP tools.

- **Foundational architecture for AI Agents**  
  Follows the [12 Factor Agents](https://github.com/humanlayer/12-factor-agents) principles for building reliable LLM applications.

- **Structured generation with BAML**  
  Uses the [BAML](https://www.boundaryml.com/) DSL to produce schema‑aware, structured outputs.

- **Tool integration via PydanticAI MCP Client**  
  Leverages the [PydanticAI MCP Client](https://ai.pydantic.dev/mcp/client/) for seamless MCP tool calls.

### Prerequisites

- Install the [uv](https://docs.astral.sh/uv/getting-started/installation/) command line tool.
- Basic level familiarity with [BAML](https://www.boundaryml.com/).
- Generate `baml_client` folder with `uv run baml-cli generate` (or the `baml` VSCode extension).
