import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class TextResponseFormat:
    type: typing.Literal["text"] = "text"

    def __str__(self) -> str:
        return "TextResponseFormat()"
