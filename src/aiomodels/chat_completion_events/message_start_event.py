import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class MessageStartEvent:
    model: str
    role: typing.Literal["assistant", "user"] = "assistant"
    name: str | None = None
    type: typing.Literal["message_start"] = "message_start"

    def __str__(self) -> str:
        return f"MessageStartEvent(model={self.model}, role={self.role}, name={self.name})"
