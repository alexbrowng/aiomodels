import typing

from anthropic.types.message_param import MessageParam
from anthropic.types.model_param import ModelParam
from anthropic.types.text_block_param import TextBlockParam
from anthropic.types.tool_param import ToolParam

from aiomodels.messages.message import Message
from aiomodels.parameters.parameters import Parameters
from aiomodels.providers.anthropic.from_message import FromMessage
from aiomodels.providers.anthropic.from_tool import FromTool
from aiomodels.response_formats.response_format import ResponseFormat
from aiomodels.tools.tool import Tool
from aiomodels.tools.tools import Tools


class RequestArgs(typing.TypedDict):
    model: ModelParam
    messages: list[MessageParam]
    max_tokens: int
    tools: typing.NotRequired[list[ToolParam]]
    temperature: typing.NotRequired[float]
    top_p: typing.NotRequired[float]
    top_k: typing.NotRequired[int]
    stop_sequences: typing.NotRequired[list[str]]
    system: typing.NotRequired[str | list[TextBlockParam]]


class FromArgs:
    @staticmethod
    def from_args(
        model: str,
        messages: list[Message],
        tools: Tools | list[Tool] | None,
        parameters: Parameters | None,
        response_format: ResponseFormat | None,
    ) -> RequestArgs:
        messages_param, system_param = FromMessage.from_messages(messages)

        request = RequestArgs(
            model=model,
            messages=messages_param,
            max_tokens=1024,
        )

        if system_param:
            request["system"] = system_param

        if tools:
            request["tools"] = FromTool.from_tools(tools)

        if parameters:
            if parameters.max_tokens is not None:
                request["max_tokens"] = parameters.max_tokens
            if parameters.temperature is not None:
                request["temperature"] = parameters.temperature
            if parameters.top_p is not None:
                request["top_p"] = parameters.top_p
            if parameters.stop:
                request["stop_sequences"] = parameters.stop

        return request
