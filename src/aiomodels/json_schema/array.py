import typing

from aiomodels.json_schema.type import JsonSchemaType


class Array(JsonSchemaType):
    """Array parameter."""

    def __init__(self, items: JsonSchemaType, description: str | None = None, nullable: bool = False):
        self._items = items
        self._description = description
        self._nullable = nullable
        self._type: typing.Literal["array"] = "array"

    @property
    def type(self) -> typing.Literal["array"]:
        return self._type

    @property
    def items(self) -> JsonSchemaType:
        return self._items

    @property
    def description(self) -> str | None:
        return self._description

    @property
    def nullable(self) -> bool:
        return self._nullable

    def to_primitives(self) -> dict:
        definition = {}
        definition["items"] = self._items.to_primitives()

        if self._nullable:
            definition["type"] = [self._type, "null"]
        else:
            definition["type"] = self._type

        if self._description:
            definition["description"] = self._description

        return definition
