import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class ToolCallStartEvent:
    id: str
    name: str
    arguments: str | None
    type: typing.Literal["tool_call_start"] = "tool_call_start"

    def __str__(self) -> str:
        return f"ToolCallStartEvent(id={self.id}, name={self.name}, arguments={self.arguments})"
