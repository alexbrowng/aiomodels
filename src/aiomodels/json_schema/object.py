import typing

from aiomodels.json_schema.property import Property
from aiomodels.json_schema.type import JsonSchemaType


class Object(JsonSchemaType):
    """Object parameter."""

    def __init__(self, *properties: Property, description: str | None = None):
        self._properties = list(properties)
        self._description = description
        self._type: typing.Literal["object"] = "object"

    @property
    def type(self) -> typing.Literal["object"]:
        return self._type

    @property
    def description(self) -> str | None:
        return self._description

    @property
    def properties(self) -> list[Property]:
        return self._properties

    def to_primitives(self) -> dict:
        definition = {
            "type": self._type,
            "properties": {property.name: property.to_primitives() for property in self._properties},
            "required": [property.name for property in self._properties if property.required],
            "additionalProperties": False,
        }

        if self._description:
            definition["description"] = self._description

        return definition
