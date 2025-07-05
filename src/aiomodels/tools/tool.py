import dataclasses

from aiomodels.json_schema.object import Object


@dataclasses.dataclass(frozen=True, slots=True)
class Tool:
    name: str
    description: str
    parameters: Object
    strict: bool = True
    instructions: str | None = None

    def __str__(self) -> str:
        return f"Tool(name={self.name}, description={self.description}, parameters={self.parameters}, strict={self.strict})"
