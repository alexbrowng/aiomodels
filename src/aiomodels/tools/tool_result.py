import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class ToolResult:
    id: str
    name: str
    result: str
    type: typing.Literal["tool_result"] = "tool_result"

    def __str__(self) -> str:
        return f"ToolResult(id={self.id}, name={self.name}, result={self.result})"
