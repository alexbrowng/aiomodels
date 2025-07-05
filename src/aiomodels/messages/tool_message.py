import dataclasses
import typing

from aiomodels.tools.tool_result import ToolResult


@dataclasses.dataclass(frozen=True, slots=True)
class ToolMessage:
    tool_result: ToolResult
    role: typing.Literal["tool"] = "tool"

    def __str__(self) -> str:
        return f"ToolMessage(tool_result={self.tool_result})"
