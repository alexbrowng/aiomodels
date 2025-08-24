import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class JsonObjectResponseFormat:
    type: typing.Literal["json_object"] = "json_object"

    def __str__(self) -> str:
        return f"JsonObjectResponseFormat(type={self.type})"
