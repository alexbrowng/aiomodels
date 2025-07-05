import dataclasses
import typing

from aiomodels.sources.base64_source import Base64Source


@dataclasses.dataclass(frozen=True, slots=True)
class ImageContent:
    source: Base64Source
    detail: typing.Literal["auto", "low", "high"] = "auto"
    type: typing.Literal["image"] = "image"

    def __str__(self) -> str:
        return f"ImageContent(source={self.source}, detail={self.detail})"
