import os
import pathlib
import sys
from collections.abc import Mapping
from dataclasses import dataclass

from loguru import logger

from baml_agents._project_utils._get_root_path import get_root_path


class _Style:
    BLACK = "black"
    BOLD = "bold"
    BLUE = "blue"
    DIM = "dim"
    CYAN = "cyan"
    NORMAL = "normal"
    GREEN = "green"
    ITALIC = "italic"
    MAGENTA = "magenta"
    UNDERLINE = "underline"
    RED = "red"
    STRIKE = "strike"
    WHITE = "white"
    REVERSE = "reverse"
    YELLOW = "yellow"


@dataclass(frozen=True)
class LogColorConfig:
    text_color: str = _Style.GREEN
    key_color: str = _Style.CYAN
    value_color: str = _Style.BLUE
    comment_color: str = _Style.MAGENTA
    keyword_color: str = _Style.GREEN


class _LogFormatter:
    """Unified formatter for both HTML and terminal log output."""

    def __init__(
        self,
        root_path,
        working_directory,
        color_config: LogColorConfig,
    ):
        self.root_path = root_path
        self.working_directory = working_directory
        self._color_config = color_config

    def filter_extras(self, record):
        filtered_extras = {}
        for key, value in record["extra"].items():
            if value is None:
                continue
            if isinstance(value, Mapping):
                formatted_value = " ".join(f"{k}={v}" for k, v in value.items())
                filtered_extras[key] = formatted_value
            elif isinstance(value, float) and value.is_integer():
                filtered_extras[key] = int(value)
            else:
                filtered_extras[key] = value
        return filtered_extras

    def format_extras(self, extras):
        if not extras:
            return ""
        items = []
        for key, value in extras.items():
            key_span = f"<{self._color_config.key_color}>{key}</{self._color_config.key_color}>"
            value_span = f"<{self._color_config.value_color}>{value}</{self._color_config.value_color}>"
            items.append(f"{key_span}={value_span}")
        return " ".join(items).replace("{", "{{").replace("}", "}}").replace("\n", "")

    def compute_filepath(self, record):
        """Compute the relative filepath for the log record."""
        filepath_root = pathlib.Path(
            f'{self.root_path}/{record["name"].replace(".", "/")}.py'
        )
        filepath_cwd = pathlib.Path(
            f'{self.working_directory}/{record["name"].replace(".", "/")}.py'
        )

        if filepath_root.exists():
            filepath = filepath_root
        elif filepath_cwd.exists():
            filepath = filepath_cwd
        else:
            return record["name"]

        relative_path = os.path.relpath(
            filepath,
            self.working_directory,
        )
        return f'./{relative_path}:{record["line"]}'

    def __call__(self, record):
        filtered_extras = self.filter_extras(record)
        formatted_extras = self.format_extras(filtered_extras)
        cc = self._color_config
        parts = [
            f"<{cc.text_color}>{{time:HH:mm:ss}}</{cc.text_color}> ",
            f"<{cc.keyword_color}><level>{{level:<8}}</level></{cc.keyword_color}> ",
            "{message}",
        ]
        if formatted_extras:
            parts.append(f" {formatted_extras}")
        parts.append(
            f" <{cc.keyword_color}><level>FROM</level></{cc.keyword_color}> <{cc.comment_color}>{{function}} <{cc.keyword_color}><level>IN</level></{cc.keyword_color}> {self.compute_filepath(record)}</{cc.comment_color}>"
        )
        return f'{"".join(parts)}\n'


def init_logging(
    level: str | None = None,
    root_path=None,
    working_directory=None,
    color_config: LogColorConfig | None = None,
):
    root_path = root_path or get_root_path()
    color_config = color_config or LogColorConfig()
    working_directory = working_directory or pathlib.Path.cwd()
    logger.remove()
    formatter = _LogFormatter(root_path, working_directory, color_config=color_config)
    logger.add(
        sys.stdout,
        format=formatter,
        level=level or "TRACE",
    )
