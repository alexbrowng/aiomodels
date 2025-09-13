import typing


class ContentBlock(typing.TypedDict):
    index: int
    type: typing.Literal["content"]


class ToolUseBlock(typing.TypedDict):
    id: str
    type: typing.Literal["tool_use"]
