import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class UrlSource:
    url: str
    type: typing.Literal["url"] = "url"

    def __str__(self) -> str:
        return f"UrlSource(url={self.url})"
