import dataclasses


@dataclasses.dataclass(frozen=True, slots=True)
class Usage:
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None

    def __str__(self) -> str:
        return f"Usage(prompt_tokens={self.prompt_tokens}, completion_tokens={self.completion_tokens}, total_tokens={self.total_tokens})"
