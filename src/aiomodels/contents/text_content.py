import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class TextContent:
    text: str
    type: typing.Literal["text"] = "text"

    def __str__(self) -> str:
        return f"TextContent(text={self.text})"
