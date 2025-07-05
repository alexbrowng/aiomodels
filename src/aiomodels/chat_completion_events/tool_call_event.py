import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class ToolCallEvent:
    id: str
    name: str
    arguments: str
    type: typing.Literal["tool_call"] = "tool_call"

    def __str__(self) -> str:
        return f"ToolCallEvent(id={self.id}, name={self.name}, arguments={self.arguments})"
