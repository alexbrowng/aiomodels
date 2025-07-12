import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class MessageUsageEvent:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    type: typing.Literal["message_usage"] = "message_usage"

    def __str__(self) -> str:
        return f"MessageUsageEvent(prompt_tokens={self.prompt_tokens}, completion_tokens={self.completion_tokens}, total_tokens={self.total_tokens})"
