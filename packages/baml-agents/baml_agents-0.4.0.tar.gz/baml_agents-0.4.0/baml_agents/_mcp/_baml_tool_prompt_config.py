from pydantic import BaseModel, ConfigDict, Field


class BamlToolPromptConfig(BaseModel):
    id_field: str = Field(default="intent", description="Field name for tool ID")
    tools_field: str = Field(
        default="intents", description="Field name for tools collection"
    )
    can_select_many: bool = Field(
        default=True, description="Allow selecting multiple tools"
    )

    model_config = ConfigDict(frozen=True)

    def output_format_prefix(self) -> str:
        id_field = self.id_field
        return (
            f"What are the next steps?\n\n"
            f"Answer in JSON format with {'one or multiple' if self.can_select_many else 'one'} of the following {id_field}s\n\n"
        )
