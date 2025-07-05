import dataclasses


@dataclasses.dataclass(frozen=True, slots=True)
class ModelPrice:
    input: float | None = None
    cached_input: float | None = None
    output: float | None = None
