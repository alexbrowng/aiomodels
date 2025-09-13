import typing


class ContentBlock(typing.TypedDict):
    index: int
    type: typing.Literal["content"]


class ToolCallBlock(typing.TypedDict):
    index: int
    id: str
    type: typing.Literal["tool_call"]
