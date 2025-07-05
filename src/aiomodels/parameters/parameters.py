import dataclasses


@dataclasses.dataclass(frozen=True, slots=True)
class Parameters:
    max_tokens: int | None = None
    temperature: float | None = None
    top_p: float | None = None
    frequency_penalty: float | None = None
    presence_penalty: float | None = None
    stop: list[str] | None = None

    def __str__(self) -> str:
        return f"Parameters(max_tokens={self.max_tokens}, temperature={self.temperature}, top_p={self.top_p}, frequency_penalty={self.frequency_penalty}, presence_penalty={self.presence_penalty}, stop={self.stop})"
