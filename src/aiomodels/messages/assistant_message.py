import dataclasses
import typing

from aiomodels.contents.json_content import JsonContent
from aiomodels.contents.refusal_content import RefusalContent
from aiomodels.contents.text_content import TextContent
from aiomodels.tools.tool_call import ToolCall


@dataclasses.dataclass(frozen=True, slots=True)
class AssistantMessage:
    content: str | typing.Sequence[TextContent | JsonContent | RefusalContent]
    tool_calls: typing.Sequence[ToolCall]
    name: str | None = None
    role: typing.Literal["assistant"] = "assistant"

    def __str__(self) -> str:
        return f"AssistantMessage(content={self.content}, tool_calls={self.tool_calls}, name={self.name})"
