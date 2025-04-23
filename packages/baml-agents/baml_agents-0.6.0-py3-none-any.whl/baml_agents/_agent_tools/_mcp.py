import hashlib
import json
import os
import shelve
import shlex
import subprocess
import threading
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from loguru import logger

from baml_agents._agent_tools._action import Action
from baml_agents._agent_tools._mcp_schema_to_type_builder._facade import (
    add_available_actions,
)
from baml_agents._agent_tools._str_result import Result
from baml_agents._agent_tools._tool_definition import McpToolDefinition
from baml_agents._agent_tools._utils._snake_to_pascal import pascal_to_snake
from baml_client.async_client import BamlCallOptions
from baml_client.type_builder import TypeBuilder


if TYPE_CHECKING:
    from pydantic import BaseModel

# Use a lock to avoid concurrent shelve access issues
_shelve_lock = threading.Lock()


def get_cache_path() -> str:
    cache_path = Path(".cache") / "mcp_cli_cache"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    return str(cache_path)


def _make_cache_key(*args) -> str:
    # Deterministically hash the arguments for a cache key
    key_str = json.dumps(args, sort_keys=True, default=str)
    return hashlib.sha256(key_str.encode("utf-8")).hexdigest()


def normalize_action_id(action_id):
    return pascal_to_snake(action_id)


class ActionRunner:
    def __init__(
        self,
        *,
        name_to_runner: dict[str, Callable] | None = None,
        cache: bool | None = None,
    ):
        self._actions = []
        self._tool_to_function = name_to_runner or {}
        self._cache = False if cache is None else cache

    def add_from_mcp_server(
        self,
        server: str,
        *,
        include: Callable[[McpToolDefinition], bool] | None = None,
        env: dict | None = None,
    ):
        tools = list_tools(server, cache=self._cache, env=env)
        for t in tools:
            if include and not include(t):
                continue
            if t.name in self._tool_to_function:
                raise ValueError(
                    f"Tool {t.name} already exists in the tool to function map."
                )
            # Use self._cache to control call_tool caching
            self._tool_to_function[normalize_action_id(t.name)] = (
                lambda params, t=t, env=env: call_tool(
                    t.name,
                    params,
                    server,
                    cache=self._cache,
                    env=env,
                )
            )
            self._actions.append(t)

    def add_action(self, action: type[Action], handler=None):
        definition = action.get_mcp_definition()
        definition.name = normalize_action_id(definition.name)
        name = definition.name
        self._actions.append(definition)
        if name in self._tool_to_function:
            raise ValueError(f"Tool {name} already exists in the tool to function map.")
        self._tool_to_function[name] = handler or (
            lambda params: action(**params).run()
        )

    def state(self) -> dict[str, Any]: ...

    def run(self, result: Any) -> Any:
        result = cast("BaseModel", result)
        action = result.model_dump()["chosen_action"]
        action_id = action["action_id"]
        action_params = {k: v for k, v in action.items() if k != "action_id"}
        if action_id not in self._tool_to_function:
            raise ValueError(
                f"Action {action_id} not found in the tool to function map."
            )

        result = self._tool_to_function[action_id](action_params)
        if isinstance(result, Result):
            return result
        return Result.from_mcp_schema(result)

    @property
    def actions(self):
        return self._actions

    def bo(self) -> BamlCallOptions:
        return {"tb": self.tb()}

    def tb(
        self, *, include: Callable[[McpToolDefinition], bool] | None = None
    ) -> TypeBuilder:
        actions = self.actions
        if include is not None:
            actions = [a for a in actions if include(a)]
        return add_available_actions("NextAction", actions, TypeBuilder())


def list_tools(
    server: str, *, cache: bool = False, env: dict | None = None
) -> list[McpToolDefinition]:
    cache_key = _make_cache_key("list_tools", server)
    if cache:
        with _shelve_lock, shelve.open(get_cache_path()) as cache_db:  # noqa: S301
            if cache_key in cache_db:
                mcp_schema = cache_db[cache_key]
            else:
                command = f"mcpt tools {server} --format json"
                mcp_schema = _run_cli_command(command, env=env)
                cache_db[cache_key] = mcp_schema
    else:
        command = f"mcpt tools {server} --format json"
        mcp_schema = _run_cli_command(command, env=env)
    return McpToolDefinition.from_mcp_schema(mcp_schema)


def call_tool(
    tool: str,
    params: dict[str, object],
    server: str,
    *,
    cache: bool = False,
    env: dict | None = None,
) -> object:
    params_json = json.dumps(params, sort_keys=True)
    cache_key = _make_cache_key("call_tool", tool, params_json, server)
    if cache:
        with _shelve_lock, shelve.open(get_cache_path()) as cache_db:  # noqa: S301
            if cache_key in cache_db:
                output = cache_db[cache_key]
            else:
                params_suffix = f" -p '{params_json}'" if params_json else ""
                command = f"mcpt call {tool}{params_suffix} {server} --format json"
                output = _run_cli_command(command, env=env)
                cache_db[cache_key] = output
    else:
        params_suffix = f" -p '{params_json}'" if params_json else ""
        command = f"mcpt call {tool}{params_suffix} {server} --format json"
        output = _run_cli_command(command, env=env)
    return json.loads(output)


def _run_cli_command(command: str | Sequence[str], *, env: dict | None = None) -> str:
    if isinstance(command, str):
        command = shlex.split(command)
    logger.debug("Running CLI command", command=command)
    result = subprocess.run(  # noqa: S603
        command,
        capture_output=True,
        text=True,
        check=False,
        env={**(env or {}), **os.environ},
    )
    if result.stderr:
        msg = f"[stderr] (exit code {result.returncode})\n{result.stderr.strip()}"
        raise RuntimeError(msg)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {result.returncode}")
    return result.stdout.strip()
