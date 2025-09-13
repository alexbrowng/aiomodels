import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class TextContent:
    text: str
    name: str | None = None
    finished: bool = True
    type: typing.Literal["text"] = "text"

    def __str__(self) -> str:
        return f"TextContent(text={self.text}, name={self.name})"

    def delta(self, delta: str) -> "TextContent":
        return TextContent(text=self.text + delta)

    def finish(self) -> "TextContent":
        return TextContent(text=self.text, name=self.name, finished=True)
