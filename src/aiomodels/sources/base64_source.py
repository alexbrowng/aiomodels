import base64
import dataclasses
import mimetypes
import pathlib
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class Base64Source:
    data: str
    media_type: str
    type: typing.Literal["base64"] = "base64"

    @property
    def url(self) -> str:
        return f"data:{self.media_type};base64,{self.data}"

    @property
    def bytes(self) -> bytes:
        return base64.b64decode(self.data)

    def __str__(self) -> str:
        return f"Base64Source(data={self.data}, media_type={self.media_type})"

    @staticmethod
    def from_file_path(file_path: pathlib.Path) -> "Base64Source":
        media_type, _ = mimetypes.guess_type(file_path)
        media_type = media_type or "application/octet-stream"

        file_bytes = file_path.read_bytes()
        data = base64.b64encode(file_bytes).decode("utf-8")

        return Base64Source(data=data, media_type=media_type)

    @staticmethod
    def from_base64_url(base64_url: str) -> "Base64Source":
        header, data = base64_url.split(";base64,")
        media_type = header.split(":")[1]

        return Base64Source(data=data, media_type=media_type)
