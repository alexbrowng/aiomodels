import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class UsageEvent:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    type: typing.Literal["usage"] = "usage"

    def __str__(self) -> str:
        return f"UsageEvent(prompt_tokens={self.prompt_tokens}, completion_tokens={self.completion_tokens}, total_tokens={self.total_tokens})"
