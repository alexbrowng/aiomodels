import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class FinishEvent:
    finish_reason: typing.Literal["stop", "tool_calls"]
    type: typing.Literal["finish"] = "finish"

    def __str__(self) -> str:
        return f"FinishEvent(finish_reason={self.finish_reason})"
