import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class ContentDeltaEvent:
    delta: str
    type: typing.Literal["content_delta"] = "content_delta"

    def __str__(self) -> str:
        return f"ContentDeltaEvent(delta={self.delta})"
