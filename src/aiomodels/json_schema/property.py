import typing

from aiomodels.json_schema.type import JsonSchemaType


class Property(JsonSchemaType):
    """Property parameter."""

    def __init__(self, name: str, parameter: JsonSchemaType, required: bool = True):
        self._name = name
        self._parameter = parameter
        self._required = required
        self._type: typing.Literal["property"] = "property"

    @property
    def name(self) -> str:
        return self._name

    @property
    def parameter(self) -> JsonSchemaType:
        return self._parameter

    @property
    def required(self) -> bool:
        return self._required

    def to_primitives(self) -> dict:
        return self.parameter.to_primitives()
