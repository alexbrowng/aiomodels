import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class JsonObjectResponseFormat:
    name: str | None = None
    type: typing.Literal["json_object"] = "json_object"

    def __str__(self) -> str:
        return f"JsonObjectResponseFormat(name={self.name}, type={self.type})"
