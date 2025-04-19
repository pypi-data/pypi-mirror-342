from abc import ABC, abstractmethod

from baml_py.baml_py import FieldType
from baml_py.type_builder import TypeBuilder
from pydantic_ai.tools import ToolDefinition

from baml_agents._mcp._json_schema_to_baml_converter import (
    AbstractJsonSchemaToBamlConverter,
)
from baml_agents._utils._python import merge_dicts_no_overlap


class AbstractToolToBamlType(ABC):

    @abstractmethod
    def convert(
        self, *, tool: ToolDefinition, tb: TypeBuilder, baml_tool_id_field: str, **_
    ) -> FieldType:
        pass


class ToolToBamlType(AbstractToolToBamlType):
    def __init__(
        self,
        *,
        schema_converter: AbstractJsonSchemaToBamlConverter,
    ):
        self._converter = schema_converter

    def convert(
        self,
        *,
        tool: ToolDefinition,
        tb: TypeBuilder,
        baml_tool_id_field: str,
    ) -> FieldType:
        schema = tool.parameters_json_schema.copy()
        props = merge_dicts_no_overlap(
            {
                baml_tool_id_field: {
                    "title": tool.name,
                    "type": tb.literal_string(tool.name),
                    "description": tool.description,
                }
            },
            schema.get("properties", {}),
        )
        schema["properties"] = props
        schema["required"] = (*schema.get("required", []), baml_tool_id_field)
        return self._converter.convert(schema, tb)
