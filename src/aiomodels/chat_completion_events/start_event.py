import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class StartEvent:
    model: str
    name: str | None = None
    type: typing.Literal["start"] = "start"

    def __str__(self) -> str:
        return f"StartEvent(model={self.model}, name={self.name})"
