import typing

from aiomodels.json_schema.type import JsonSchemaType


class String(JsonSchemaType):
    """String parameter."""

    def __init__(self, description: str | None = None, default: str | None = None, nullable: bool = False):
        self._description = description
        self._default = default
        self._nullable = nullable
        self._type: typing.Literal["string"] = "string"

    @property
    def type(self) -> typing.Literal["string"]:
        return self._type

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

        if self._nullable:
            definition["type"] = [self._type, "null"]
        else:
            definition["type"] = self._type

        if self._description:
            definition["description"] = self._description

        if self._default:
            definition["default"] = self._default

        return definition
