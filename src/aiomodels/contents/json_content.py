import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class JsonContent:
    json: str
    type: typing.Literal["json"] = "json"

    def __str__(self) -> str:
        return f"JsonContent(json={self.json})"
