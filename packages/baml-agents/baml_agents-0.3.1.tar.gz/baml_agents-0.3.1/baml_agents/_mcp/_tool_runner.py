import asyncio
import warnings
from abc import ABC, abstractmethod

from mcp.types import CallToolResult
from pydantic import BaseModel
from pydantic_ai.mcp import MCPServer

from baml_agents._mcp._baml_tool_prompt_config import BamlToolPromptConfig


class AbstractToolInvoker(ABC):
    """Defines the API for dispatching tool calls against an MCP server."""

    @abstractmethod
    async def run(self, calls: list[dict]) -> list[CallToolResult]: ...


class ToolRunner(AbstractToolInvoker):
    """Invokes tool calls returned by the LLM against the MCP server."""

    def __init__(self, *, server: MCPServer, prompt_cfg: BamlToolPromptConfig):
        self._server = server
        self._prompt_cfg = prompt_cfg

    async def run(self, result: BaseModel) -> list[CallToolResult]:
        """Run the tool calls from the result."""
        tool_calls: list[dict] | None = getattr(
            result, self._prompt_cfg.tools_field, None
        )
        if isinstance(result, dict) and self._prompt_cfg.id_field in result:
            tool_calls = [result]
        if tool_calls is None:
            raise ValueError(
                "Could not find tool calls in the result. Currently only root level tool calls are supported."
            )

        if self._should_warn_multiple_tools(tool_calls):
            self._warn_multiple_tools(len(tool_calls))

        return await self.run_tools(tool_calls)

    def _should_warn_multiple_tools(self, tool_calls) -> bool:
        return (
            not self._prompt_cfg.can_select_many
            and isinstance(tool_calls, list)
            and len(tool_calls) > 1
        )

    def _warn_multiple_tools(self, count: int) -> None:
        warnings.warn(
            f"Multiple tool calls provided ({count}) but only one is expected "
            f"(can_select_many=False). All will be executed.",
            UserWarning,
            stacklevel=2,
        )

    async def run_tools(self, tool_calls: list[dict]) -> list[CallToolResult]:
        return await asyncio.gather(
            *[
                self._server.call_tool(
                    call[self._prompt_cfg.id_field],
                    {k: v for k, v in call.items() if k != self._prompt_cfg.id_field},
                )
                for call in tool_calls
            ]
        )
