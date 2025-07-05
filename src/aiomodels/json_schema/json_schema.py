import dataclasses

from aiomodels.json_schema.object import Object


@dataclasses.dataclass(frozen=True, slots=True)
class JsonSchema:
    name: str
    description: str
    strict: bool
    schema: Object

    def __str__(self) -> str:
        return (
            f"JsonSchema(name={self.name}, description={self.description}, strict={self.strict}, schema={self.schema})"
        )
