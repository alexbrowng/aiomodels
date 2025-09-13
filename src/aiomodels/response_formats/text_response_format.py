import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class TextResponseFormat:
    name: str | None = None
    type: typing.Literal["text"] = "text"

    def __str__(self) -> str:
        return f"TextResponseFormat(name={self.name})"
