import dataclasses
import typing

from aiomodels.contents.audio_content import AudioContent
from aiomodels.contents.document_content import DocumentContent
from aiomodels.contents.image_content import ImageContent
from aiomodels.contents.text_content import TextContent


@dataclasses.dataclass(frozen=True, slots=True)
class UserMessage:
    content: str | typing.Sequence[TextContent | ImageContent | DocumentContent | AudioContent]
    name: str | None = None
    role: typing.Literal["user"] = "user"

    def __str__(self) -> str:
        return f"UserMessage(content={self.content}, name={self.name})"
