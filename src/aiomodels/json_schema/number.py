import typing

from aiomodels.json_schema.type import JsonSchemaType


class Number(JsonSchemaType):
    """Number parameter."""

    def __init__(
        self,
        description: str | None = None,
        default: float | None = None,
        nullable: bool = False,
        minimum: float | None = None,
        maximum: float | None = None,
    ):
        self._description = description
        self._default = default
        self._nullable = nullable
        self._minimum = minimum
        self._maximum = maximum
        self._type: typing.Literal["number"] = "number"

    @property
    def type(self) -> typing.Literal["number"]:
        return self._type

    @property
    def description(self) -> str | None:
        return self._description

    @property
    def default(self) -> float | None:
        return self._default

    @property
    def nullable(self) -> bool:
        return self._nullable

    @property
    def minimum(self) -> float | None:
        return self._minimum

    @property
    def maximum(self) -> float | None:
        return self._maximum

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

        if self._minimum:
            definition["minimum"] = self._minimum

        if self._maximum:
            definition["maximum"] = self._maximum

        return definition
