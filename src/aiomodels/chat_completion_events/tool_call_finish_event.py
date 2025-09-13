import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class ToolCallFinishEvent:
    id: str
    type: typing.Literal["tool_call_finish"] = "tool_call_finish"

    def __str__(self) -> str:
        return f"ToolCallFinishEvent(id={self.id})"
