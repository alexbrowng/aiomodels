import dataclasses
import typing

from aiomodels.sources.base64_source import Base64Source


@dataclasses.dataclass(frozen=True, slots=True)
class DocumentContent:
    source: Base64Source
    name: str
    type: typing.Literal["file"] = "file"

    def __str__(self) -> str:
        return f"DocumentContent(name={self.name}, source={self.source})"
