import typing

from aiomodels.json_schema.type import JsonSchemaType


class Enum(JsonSchemaType):
    """Enum parameter."""

    def __init__(
        self, choices: list[str], description: str | None = None, default: str | None = None, nullable: bool = False
    ):
        self._description = description
        self._default = default
        self._nullable = nullable
        self._choices = choices
        self._type: typing.Literal["enum"] = "enum"

    @property
    def type(self) -> typing.Literal["enum"]:
        return self._type

    @property
    def choices(self) -> list[str]:
        return self._choices

    @property
    def description(self) -> str | None:
        return self._description

    @property
    def default(self) -> str | None:
        return self._default

    @property
    def nullable(self) -> bool:
        return self._nullable

    def to_primitives(self) -> dict:
        definition = {}
        definition["enum"] = self._choices

        if self._nullable:
            definition["type"] = ["string", "null"]
        else:
            definition["type"] = "string"

        if self._description:
            definition["description"] = self._description

        if self._default:
            definition["default"] = self._default

        return definition
