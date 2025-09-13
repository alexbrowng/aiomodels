import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class MessageFinishEvent:
    reason: typing.Literal["stop", "tool_calls", "length"]
    type: typing.Literal["message_finish"] = "message_finish"

    def __str__(self) -> str:
        return f"MessageFinishEvent(reason={self.reason})"
