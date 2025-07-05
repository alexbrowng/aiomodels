import dataclasses


@dataclasses.dataclass(frozen=True, slots=True)
class ToolResult:
    id: str
    name: str
    result: str

    def __str__(self) -> str:
        return f"ToolResult(id={self.id}, name={self.name}, result={self.result})"
