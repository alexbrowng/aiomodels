import dataclasses
import typing

from aiomodels.messages.assistant_message import AssistantMessage
from aiomodels.usage.usage import Usage


@dataclasses.dataclass(frozen=True, slots=True)
class ChatCompletion:
    finish_reason: typing.Literal["stop", "tool_calls"]
    message: AssistantMessage
    usage: Usage | None = None

    def __str__(self) -> str:
        return f"ChatCompletion(finish_reason={self.finish_reason}, message={self.message}, usage={self.usage})"
