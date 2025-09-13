import json
import typing

from anthropic.types import Message as AnthropicMessage

from aiomodels.chat_completions.chat_completion import ChatCompletion
from aiomodels.contents.json_content import JsonContent
from aiomodels.contents.text_content import TextContent
from aiomodels.messages.assistant_message import AssistantMessage
from aiomodels.response_formats.json_object_response_format import JsonObjectResponseFormat
from aiomodels.response_formats.json_schema_response_format import JsonSchemaResponseFormat
from aiomodels.response_formats.response_format import ResponseFormat
from aiomodels.tools.tool_call import ToolCall
from aiomodels.usage.usage import Usage


class ToChatCompletion:
    @staticmethod
    def finish_reason(message: AnthropicMessage) -> typing.Literal["stop", "tool_calls", "length"]:
        finish_reason = "stop"
        if message.stop_reason == "tool_use":
            finish_reason = "tool_calls"
        elif message.stop_reason == "max_tokens":
            finish_reason = "length"

        return finish_reason

    @staticmethod
    def usage(message: AnthropicMessage) -> Usage:
        return Usage(
            message.usage.input_tokens,
            message.usage.output_tokens,
            message.usage.input_tokens + message.usage.output_tokens,
        )

    @staticmethod
    def message(
        message: AnthropicMessage,
        response_format: ResponseFormat | None = None,
        message_name: str | None = None,
    ) -> AssistantMessage:
        content = []
        tool_calls = []

        for block in message.content:
            if block.type == "text":
                if isinstance(response_format, JsonSchemaResponseFormat):
                    content.append(JsonContent(json=block.text, name=response_format.json_schema.name))
                elif isinstance(response_format, JsonObjectResponseFormat):
                    content.append(JsonContent(json=block.text, name=response_format.name))
                else:
                    content_name = response_format.name if response_format else None
                    content.append(TextContent(text=block.text, name=content_name))
            elif block.type == "tool_use":
                tool_calls.append(
                    ToolCall(
                        id=block.id,
                        name=block.name,
                        arguments=json.dumps(block.input, default=str) if isinstance(block.input, dict) else None,
                    )
                )

        return AssistantMessage(
            role="assistant",
            content=content,
            tool_calls=tool_calls,
            name=message_name,
        )

    @staticmethod
    def from_message(
        message: AnthropicMessage,
        response_format: ResponseFormat | None = None,
        message_name: str | None = None,
    ) -> ChatCompletion:
        return ChatCompletion(
            finish_reason=ToChatCompletion.finish_reason(message),
            message=ToChatCompletion.message(message, response_format, message_name),
            usage=ToChatCompletion.usage(message),
        )
