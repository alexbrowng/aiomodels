import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class ToolCall:
    id: str
    name: str
    arguments: str | None
    finished: bool = True
    type: typing.Literal["tool_call"] = "tool_call"

    def __str__(self) -> str:
        return f"ToolCall(id={self.id}, name={self.name}, arguments={self.arguments})"

    def delta(self, delta: str) -> "ToolCall":
        arguments = self.arguments + delta if self.arguments else delta
        return ToolCall(id=self.id, name=self.name, arguments=arguments)

    def finish(self) -> "ToolCall":
        return ToolCall(id=self.id, name=self.name, arguments=self.arguments, finished=True)
