import dataclasses


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

    def __str__(self) -> str:
        return f"Parameters(max_tokens={self.max_tokens}, temperature={self.temperature}, top_p={self.top_p}, top_k={self.top_k}, frequency_penalty={self.frequency_penalty}, repetition_penalty={self.repetition_penalty}, presence_penalty={self.presence_penalty}, seed={self.seed}, stop={self.stop})"
