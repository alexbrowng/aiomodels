import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class SystemMessage:
    content: str
    name: str | None = None
    role: typing.Literal["system"] = "system"

    def __str__(self) -> str:
        return f"SystemMessage(content={self.content}, name={self.name})"
