from __future__ import annotations

from contextlib import AsyncExitStack, asynccontextmanager
from typing import (
    Any,
    AsyncIterator,
    Callable,
    Dict,
    Iterable,
    List,
    Self,
    Sequence,
    Tuple,
    TypeVar,
)

from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream
from baml_py.type_builder import TypeBuilder
from mcp.types import CallToolResult, JSONRPCMessage, TextContent
from pydantic_ai.mcp import MCPServer
from pydantic_ai.tools import ToolDefinition

from baml_agents._mcp._baml_tool_prompt_config import BamlToolPromptConfig
from baml_agents._mcp._json_schema_to_baml_converter import JsonSchemaToBamlConverter
from baml_agents._mcp._tool_runner import ToolRunner
from baml_agents._mcp._tool_to_baml_type import ToolToBamlType
from baml_agents._mcp._type_builder_orchestrator import TypeBuilderOrchestrator

T = TypeVar("T", bound=TypeBuilder)


class DuplicateToolNameError(ValueError):
    """Raised when tool name collision occurs."""


class McpServers(MCPServer):
    """Aggregates multiple MCP Server instances into a unified service."""

    __slots__ = (
        "_servers",
        "_server_map",
        "_tools",
        "_exit_stack",
        "_exit_stack_factory",
    )

    def __init__(
        self,
        servers: Sequence[MCPServer],
        *,
        exit_stack_factory: Callable[[], AsyncExitStack] | None = None,
    ) -> None:
        self._servers = list(servers)
        self._server_map: Dict[str, MCPServer] = {}
        self._tools: List[ToolDefinition] = []
        self._exit_stack: AsyncExitStack | None = None
        self._exit_stack_factory = exit_stack_factory

    async def __aenter__(self) -> Self:
        """Enter all servers and preload tools."""
        if self._exit_stack_factory is not None:
            self._exit_stack = self._exit_stack_factory()
        else:
            self._exit_stack = AsyncExitStack()
        await self._enter_servers()
        await self._cache_tools()

        return self

    async def __aexit__(
        self, exc_type: type | None, exc_val: BaseException | None, exc_tb: Any
    ) -> None:
        """Exit all servers and clear cache."""
        if self._exit_stack is not None:
            await self._exit_stack.aclose()
            self._exit_stack = None
        self._tools.clear()
        self._server_map.clear()

    async def _enter_servers(self) -> None:
        """Async enter each server in its own context."""
        assert self._exit_stack is not None
        for idx, server in enumerate(self._servers):
            entered = await self._exit_stack.enter_async_context(server)
            self._servers[idx] = entered

    async def _cache_tools(self) -> None:
        """Load tools and map names to their servers."""
        for server in self._servers:
            for tool in await server.list_tools():
                if tool.name in self._server_map:
                    prev_server = self._server_map[tool.name]
                    raise DuplicateToolNameError(
                        f"Duplicate tool: {tool.name!r} found in both servers: "
                        f"{repr(prev_server)} and {repr(server)}"
                    )
                self._server_map[tool.name] = server
                self._tools.append(tool)

    async def list_tools(self) -> List[ToolDefinition]:
        """List of available ToolDefinition objects."""
        return list(self._tools)

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> CallToolResult:
        """Invoke the named tool with provided arguments."""
        server = self._server_map.get(name)
        if not server:
            return CallToolResult(
                content=[
                    TextContent(type="text", text=f"Error: Tool '{name}' not found.")
                ],
                isError=True,
            )
        return await server.call_tool(name, arguments)

    async def build_tool_types(
        self,
        builder: T,
        output_class,
        *,
        tools: Iterable[ToolDefinition] | None = None,
        prompt_cfg: BamlToolPromptConfig | None = None,
    ) -> Tuple[T, ToolRunner, str]:
        prompt_cfg = prompt_cfg or BamlToolPromptConfig()
        schema_converter = JsonSchemaToBamlConverter()
        tool_converter = ToolToBamlType(schema_converter=schema_converter)
        tbo = TypeBuilderOrchestrator(
            tool_converter=tool_converter, prompt_cfg=prompt_cfg
        )
        tb = await tbo.build_types(
            builder, output_class, tools=tools or await self.list_tools()
        )
        invoker = ToolRunner(server=self, prompt_cfg=prompt_cfg)
        return tb, invoker, prompt_cfg.output_format_prefix()

    @asynccontextmanager
    async def client_streams(
        self,
    ) -> AsyncIterator[
        tuple[
            MemoryObjectReceiveStream[JSONRPCMessage | Exception],
            MemoryObjectSendStream[JSONRPCMessage],
        ]
    ]:
        raise NotImplementedError("Not implemented for McpServers")
        yield
