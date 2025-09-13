import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class JsonContent:
    json: str
    name: str | None = None
    finished: bool = True
    type: typing.Literal["json"] = "json"

    def __str__(self) -> str:
        return f"JsonContent(json={self.json}, name={self.name})"

    def delta(self, delta: str) -> "JsonContent":
        return JsonContent(json=self.json + delta)

    def finish(self) -> "JsonContent":
        return JsonContent(json=self.json, name=self.name, finished=True)
