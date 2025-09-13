import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class ContentFinishEvent:
    index: int
    type: typing.Literal["content_finish"] = "content_finish"

    def __str__(self) -> str:
        return f"ContentFinishEvent(index={self.index})"
