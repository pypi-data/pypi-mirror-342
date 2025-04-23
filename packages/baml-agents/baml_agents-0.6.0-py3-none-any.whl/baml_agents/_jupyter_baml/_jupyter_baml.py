import asyncio
import html
import json
import uuid
from collections.abc import Callable
from contextlib import contextmanager
from pprint import pformat
from typing import Any, Generic, Literal, TypeVar, cast

from baml_py import Collector
from IPython.display import Javascript, display

from ._jupyter_button_hide import (
    hide_text_under_a_button,
    hide_text_under_a_button_nested,
)
from ._sole import sole
from ._token_cost_estimator import TokenCostEstimator

T = TypeVar("T")


def _format_price_and_duration(
    cost_usd_per_thousand: float, duration_ms: int | None
) -> str:
    duration_sec = f"{duration_ms/1000:.2f}s" if duration_ms is not None else "N/A"
    return f"{cost_usd_per_thousand:.2f}$/1k, {duration_sec}"


def _get_call_duration_ms(call) -> int | None:
    timing = getattr(call, "timing", None)
    if timing is not None:
        return getattr(timing, "duration_ms", None)
    return None


def _get_log_duration_ms(log) -> int | None:
    timing = getattr(log, "timing", None)
    if timing is not None:
        return getattr(timing, "duration_ms", None)
    return None


class _StreamingInterceptorWrapper:
    def __init__(self, ai: Any, callback: Callable, /):
        self._ai = ai
        self._callback = callback

    def __getattribute__(self, name: str) -> Any:
        ai_instance = object.__getattribute__(self, "_ai")
        callback = object.__getattribute__(self, "_callback")
        if name in {
            "_ai",
            "_callback",
            "__class__",
            "__init__",
            "__getattribute__",
            "__dict__",
            "__await__",
            "__aiter__",
            "__anext__",
        }:
            return object.__getattribute__(self, name)

        attr = getattr(ai_instance.stream, name)

        async def wrapper(*args, **kwargs):
            stream_obj = attr(*args, **kwargs)
            async for partial in stream_obj:
                callback(partial)
            final_response = await stream_obj.get_final_response()
            callback(final_response)
            return final_response

        wrapper.__name__ = name
        wrapper.__qualname__ = f"{type(self).__name__}.{name}"
        wrapper.__doc__ = getattr(attr, "__doc__", None)
        wrapper.__annotations__ = getattr(attr, "__annotations__", {})

        return wrapper


class JupyterBamlStreamer:
    """
    Context manager that:
      - Renders pretty <pre> formatted output (preserves whitespace and newlines).
      - Updates the content efficiently via Jupyter's display_id mechanism.
      - Removes the HTML element on exit, hiding the output when done.
    """

    def __init__(
        self,
        initial_message: str = "Initializing…",
        *,
        display_id: str | None = None,
        clear_after_finish: bool = True,
    ):
        self.display_id = display_id or f"stream-{uuid.uuid4()}"
        self.clear_after_finish = clear_after_finish
        escaped_msg = html.escape(initial_message, quote=False)
        self._initial_html = f'<pre id="{self.display_id}">{escaped_msg}</pre>'
        self._active = False
        self._handle = None

    @contextmanager
    def session(self):
        """
        Context manager for JupyterBamlStreamer.
        Usage:
            with streamer.session():
                ...
        """
        if not self._active:
            self._handle = display(
                {"text/html": self._initial_html},
                display_id=self.display_id,
                raw=True,
            )
            self._active = True
        try:
            yield self
        finally:
            if self.clear_after_finish and self._active:
                js = f"""
                (function(){{
                  var el = document.getElementById("{self.display_id}");
                  if (el) el.remove();
                }})();
                """
                display(Javascript(js))
            self._active = False
            self._handle = None

    def update(self, data, *, use_br: bool = False):
        if not isinstance(data, str):
            try:
                s = data.model_dump_json(indent=4)
            except AttributeError:
                s = json.dumps(data, indent=4)
        else:
            s = data

        escaped = html.escape(s, quote=False)

        if use_br:
            html_body = escaped.replace("\n", "<br>")
            new_html = (
                f'<div id="{self.display_id}" style="font-family:monospace">'
                f"{html_body}</div>"
            )
        else:
            new_html = f'<pre id="{self.display_id}">{escaped}</pre>'

        if self._handle is None:
            raise RuntimeError(
                "Display handle is None. Did you forget to enter the context manager?"
            )
        self._handle.update({"text/html": new_html}, raw=True)

    def show(self, result):
        self.update(pformat(result.model_dump(), width=200, sort_dicts=False))


class JupyterBamlCollector(Generic[T]):
    def __init__(
        self,
        ai: T,
        *,
        stream_callback: Callable | None = None,
        intent_summarizer: Callable | None = None,
    ):
        self._original_ai = ai
        self.collector = Collector(name="collector")
        self._ai = self._original_ai.with_options(collector=self.collector)  # type: ignore
        self.cost_estimator = TokenCostEstimator()
        self._stream_callback = stream_callback
        self._intent_summarizer = intent_summarizer

    @property
    def ai(self) -> T:
        if self._stream_callback:
            return _StreamingInterceptorWrapper(self._ai, self._stream_callback)  # type: ignore
        return self._ai

    @property
    def b(self) -> T:
        return self.ai

    @staticmethod
    def _format_log_messages(messages):
        prompt_parts = []
        for message in messages:
            content = sole(message["content"])
            if content["type"] != "text":
                raise ValueError(
                    f"Expected content type 'text', but got '{content['type']}'"
                )
            prompt_parts.append(f"[{message['role']}]\n{content['text']}")
        return "\n\n".join(prompt_parts)

    def _get_prompt_buttons(self, calls, *, omit_cost_and_model: bool = False):
        ret = {}
        for call in calls:
            request_body = call.http_request.body.json()
            messages = request_body["messages"]

            cost = self.cost_estimator.calculate_cost(
                request_body["model"],
                call.usage.input_tokens,
                call.usage.output_tokens,
            )
            cost_usd_per_thousand = cost["total_cost_usd"] * 1_000
            duration_ms = _get_call_duration_ms(call)

            formatted = self._format_log_messages(messages)
            if omit_cost_and_model:
                label = f"Request: ({len(messages)} message{'s' if len(messages) > 1 else ''})"
            else:
                price_and_duration = _format_price_and_duration(
                    cost_usd_per_thousand, duration_ms
                )
                label = (
                    f"Request: ({len(messages)} message{'s' if len(messages) > 1 else ''}) "
                    f"{price_and_duration} ({cost['model_info']['model_name']})"
                )
            ret[label] = formatted
        return ret

    async def _get_completion_button(
        self, raw_llm_response, log=None, *, omit_cost_and_model: bool = False
    ):
        summary_label = None
        if self._intent_summarizer is not None:
            summary_label = await self._intent_summarizer(raw_llm_response)
            # Defensive: fallback to default label if summarizer fails
            summary_label = None

        response_str = str(raw_llm_response).replace('"', "")
        action_count = response_str.count("action:")
        tool_count = response_str.count("tool:")
        suffix = self._get_suffix(action_count, tool_count)
        price_and_duration = ""
        model_name = ""
        if not omit_cost_and_model and log is not None and log.calls:
            last_call = log.calls[-1]
            request_body = last_call.http_request.body.json()
            cost = self.cost_estimator.calculate_cost(
                request_body["model"],
                last_call.usage.input_tokens,
                last_call.usage.output_tokens,
            )
            cost_usd_per_thousand = cost["total_cost_usd"] * 1_000
            duration_ms = _get_call_duration_ms(last_call)
            price_and_duration = (
                f" { _format_price_and_duration(cost_usd_per_thousand, duration_ms) }"
            )
            model_name = f" ({cost['model_info']['model_name']})"
        # Use summarizer output as label if available, else fallback to default
        if summary_label is not None:
            label = f"Response: {summary_label}"
        else:
            label = f"Completion{suffix}"
            if not omit_cost_and_model:
                label += f"{price_and_duration}{model_name}"
        return label, str(raw_llm_response)

    async def display_calls(
        self,
        *,
        prompts: Literal["always_hide", "always_show", "show", "hide"] = "hide",
        completions: Literal["always_hide", "always_show", "show", "hide"] = "hide",
    ):
        def get_key(i, k):
            return f"Step {i} - {k}"

        logs = list(self.collector.logs)
        completion_button_coros = [
            (
                self._get_completion_button(log.raw_llm_response, log=log)
                if completions != "always_hide"
                else None
            )
            for log in logs
        ]
        completion_buttons = (
            await asyncio.gather(
                *[coro for coro in completion_button_coros if coro is not None]
            )
            if completions != "always_hide"
            else []
        )

        completion_idx = 0
        for i, log in enumerate(logs, start=1):
            if prompts != "always_hide":
                for k, v in self._get_prompt_buttons(log.calls).items():
                    hide_text_under_a_button(get_key(i, k), v, visibility=prompts)
            if completions != "always_hide":
                k, v = completion_buttons[completion_idx]
                hide_text_under_a_button(get_key(i, k), v, visibility=completions)
                completion_idx += 1

    async def display_session(self, root_name: str, *, show_depth=0):
        nested_buttons = {}

        logs = self.collector.logs

        # Prepare prompt buttons and gather completion button coroutines
        completion_button_coros = []
        prompt_buttons_list = []
        for log in logs:
            # Compute cost/model info for each call (side effect, not used here)
            total_cost_usd_per_thousand = 0
            all_models = set()
            for call in log.calls:
                if call.http_request is None:
                    continue
                request_body = call.http_request.body.json()
                cost = self.cost_estimator.calculate_cost(
                    request_body["model"],
                    call.usage.input_tokens,
                    call.usage.output_tokens,
                )
                cost_usd_per_thousand = cost["total_cost_usd"] * 1_000
                total_cost_usd_per_thousand += cost_usd_per_thousand
                all_models.add(cost["model_info"]["model_name"])
            # Collect prompt buttons for this log
            prompt_buttons = dict(
                self._get_prompt_buttons(log.calls, omit_cost_and_model=False).items()
            )
            prompt_buttons_list.append(prompt_buttons)
            # Prepare coroutine for completion button
            completion_button_coros.append(
                self._get_completion_button(
                    log.raw_llm_response, log=log, omit_cost_and_model=True
                )
            )

        # Gather all completion buttons concurrently
        completion_buttons = await asyncio.gather(*completion_button_coros)

        # Update nested_buttons with prompt and completion buttons
        for prompt_buttons, (k, v) in zip(
            prompt_buttons_list, completion_buttons, strict=True
        ):
            nested_buttons.update(prompt_buttons)
            nested_buttons[k] = v
        hide_text_under_a_button_nested(
            f"{root_name}, Cost: {self.format_total_cost()}",
            nested_buttons,
            visibility="show",
            hide_after_level=show_depth,
        )

    def format_total_cost(self):
        all_models = set()
        total_cost_usd_per_thousand = 0
        total_duration_ms = 0
        for log in self.collector.logs:
            log_duration_ms = _get_log_duration_ms(log)
            if log_duration_ms is not None:
                total_duration_ms += log_duration_ms
            for call in log.calls:
                if call.http_request is None:
                    raise ValueError(
                        "Expected call.http_request to be not None, but got None"
                    )
                request_body = call.http_request.body.json()
                cost = self.cost_estimator.calculate_cost(
                    request_body["model"],
                    call.usage.input_tokens,
                    call.usage.output_tokens,
                )
                cost_usd_per_thousand = cost["total_cost_usd"] * 1_000
                total_cost_usd_per_thousand += cost_usd_per_thousand
                all_models.add(cost["model_info"]["model_name"])

        duration_sec = f"{total_duration_ms/1000:.2f}s" if total_duration_ms else "N/A"
        return f"{total_cost_usd_per_thousand:.2f}$/1k, {duration_sec} ({', '.join(all_models)})"

    @staticmethod
    def _get_suffix(
        action_count: int,
        tool_count: int,
    ) -> str:
        action_part = f"action: {action_count}" if action_count else ""
        tool_part = f"tool: {tool_count}" if tool_count else ""

        if action_part and tool_part:
            return f" ({action_part}, {tool_part})"
        if action_part:
            return f" ({action_part})"
        if tool_part:
            return f" ({tool_part})"
        return ""


class JupyterBamlMonitor(Generic[T]):
    def __init__(self, ai: T, *, summarizer=None):
        self._ai = ai
        self._summarizer = summarizer
        self._streamer: JupyterBamlStreamer | None = None
        self._collector: JupyterBamlCollector | None = None

    @property
    def ai(self) -> T:
        if self._collector is None:
            raise RuntimeError("JupyterTraceLLMCalls tracer has not been initialized.")
        return cast("T", self._collector.ai)

    async def display_calls(
        self,
        *,
        prompts: Literal["always_hide", "always_show", "show", "hide"] = "hide",
        completions: Literal["always_hide", "always_show", "show", "hide"] = "hide",
    ):
        if self._collector is None:
            raise RuntimeError("JupyterTraceLLMCalls tracer has not been initialized.")
        await self._collector.display_calls(prompts=prompts, completions=completions)

    async def display_session(self, name: str):
        if self._collector is None:
            raise RuntimeError("JupyterTraceLLMCalls tracer has not been initialized.")
        await self._collector.display_session(name)

    @contextmanager
    def session(self):
        with JupyterBamlStreamer(clear_after_finish=True).session() as streamer:
            self._streamer = streamer
            self._collector = JupyterBamlCollector(
                self._ai,
                stream_callback=streamer.show,
                intent_summarizer=self._summarizer,
            )
            try:
                yield self
            finally:
                self._streamer = None
