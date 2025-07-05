import dataclasses
import typing

from aiomodels.json_schema.json_schema import JsonSchema


@dataclasses.dataclass(frozen=True, slots=True)
class JsonSchemaResponseFormat:
    json_schema: JsonSchema
    type: typing.Literal["json_schema"] = "json_schema"

    def __str__(self) -> str:
        return f"JsonSchemaResponseFormat(json_schema={self.json_schema}, type={self.type})"
