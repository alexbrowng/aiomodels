import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class ModelPrice:
    input: float | None = None
    cached_input: float | None = None
    output: float | None = None
    type: typing.Literal["model_price"] = "model_price"

    def __str__(self) -> str:
        return f"ModelPrice(input={self.input}, cached_input={self.cached_input}, output={self.output})"
