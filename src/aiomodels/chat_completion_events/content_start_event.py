import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class ContentStartEvent:
    index: int
    content_type: typing.Literal["text", "json"] = "text"
    content: str | None = None
    name: str | None = None
    type: typing.Literal["content_start"] = "content_start"

    def __str__(self) -> str:
        return f"ContentStartEvent(index={self.index}, content_type={self.content_type}, content={self.content}, name={self.name})"
