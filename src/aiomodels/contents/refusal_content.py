import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class RefusalContent:
    refusal: str
    type: typing.Literal["refusal"] = "refusal"

    def __str__(self) -> str:
        return f"RefusalContent(refusal={self.refusal})"
