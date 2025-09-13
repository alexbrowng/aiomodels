import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class Parameters:
    max_tokens: int | None = None
    temperature: float | None = None
    top_p: float | None = None
    top_k: int | None = None
    frequency_penalty: float | None = None
    repetition_penalty: float | None = None
    presence_penalty: float | None = None
    seed: int | None = None
    stop: list[str] | None = None
    type: typing.Literal["parameters"] = "parameters"

    def __str__(self) -> str:
        return f"Parameters(max_tokens={self.max_tokens}, temperature={self.temperature}, top_p={self.top_p}, top_k={self.top_k}, frequency_penalty={self.frequency_penalty}, repetition_penalty={self.repetition_penalty}, presence_penalty={self.presence_penalty}, seed={self.seed}, stop={self.stop})"

    def __add__(self, other: "Parameters") -> "Parameters":
        return Parameters(
            max_tokens=other.max_tokens if other.max_tokens is not None else self.max_tokens,
            temperature=other.temperature if other.temperature is not None else self.temperature,
            top_p=other.top_p if other.top_p is not None else self.top_p,
            top_k=other.top_k if other.top_k is not None else self.top_k,
            frequency_penalty=other.frequency_penalty
            if other.frequency_penalty is not None
            else self.frequency_penalty,
            presence_penalty=other.presence_penalty if other.presence_penalty is not None else self.presence_penalty,
            repetition_penalty=other.repetition_penalty
            if other.repetition_penalty is not None
            else self.repetition_penalty,
            seed=other.seed if other.seed is not None else self.seed,
            stop=other.stop if other.stop is not None else self.stop,
        )
