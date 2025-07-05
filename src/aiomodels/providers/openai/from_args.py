import typing

from openai.types.chat import ChatCompletionToolParam
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.shared_params.response_format_json_schema import ResponseFormatJSONSchema
from openai.types.shared_params.response_format_text import ResponseFormatText

from aiomodels.messages.message import Message
from aiomodels.parameters.parameters import Parameters
from aiomodels.providers.openai.from_message import FromMessage
from aiomodels.providers.openai.from_response_format import FromResponseFormat
from aiomodels.providers.openai.from_tool import FromTool
from aiomodels.response_formats.response_format import ResponseFormat
from aiomodels.tools.tool import Tool
from aiomodels.tools.tools import Tools


class RequestArgs(typing.TypedDict):
    model: str
    messages: list[ChatCompletionMessageParam]
    tools: typing.NotRequired[list[ChatCompletionToolParam]]
    temperature: typing.NotRequired[float]
    top_p: typing.NotRequired[float]
    max_tokens: typing.NotRequired[int]
    frequency_penalty: typing.NotRequired[float]
    presence_penalty: typing.NotRequired[float]
    response_format: typing.NotRequired[ResponseFormatText | ResponseFormatJSONSchema]
    stop: typing.NotRequired[list[str]]


class FromArgs:
    @staticmethod
    def from_args(
        model: str,
        messages: list[Message],
        tools: Tools | list[Tool] | None,
        parameters: Parameters | None,
        response_format: ResponseFormat | None,
    ) -> RequestArgs:
        request = RequestArgs(
            model=model,
            messages=[FromMessage.from_message(message) for message in messages],
        )

        if tools:
            request["tools"] = FromTool.from_tools(tools)

        if parameters:
            if parameters.temperature is not None:
                request["temperature"] = parameters.temperature
            if parameters.top_p is not None:
                request["top_p"] = parameters.top_p
            if parameters.max_tokens is not None:
                request["max_tokens"] = parameters.max_tokens
            if parameters.frequency_penalty is not None:
                request["frequency_penalty"] = parameters.frequency_penalty
            if parameters.presence_penalty is not None:
                request["presence_penalty"] = parameters.presence_penalty
            if parameters.stop:
                request["stop"] = parameters.stop

        if response_format:
            request["response_format"] = FromResponseFormat.from_response_format(response_format)

        return request
