import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class ToolCallDeltaEvent:
    id: str
    arguments: str
    type: typing.Literal["tool_call_delta"] = "tool_call_delta"

    def __str__(self) -> str:
        return f"ToolCallDeltaEvent(id={self.id}, arguments={self.arguments})"
