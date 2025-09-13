import json
import typing

from types_aiobotocore_bedrock_runtime.type_defs import ConverseResponseTypeDef

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
    def usage(converse_response: ConverseResponseTypeDef) -> Usage:
        return Usage(
            prompt_tokens=converse_response["usage"]["inputTokens"],
            completion_tokens=converse_response["usage"]["outputTokens"],
            total_tokens=converse_response["usage"]["totalTokens"],
        )

    @staticmethod
    def finish_reason(converse_response: ConverseResponseTypeDef) -> typing.Literal["stop", "tool_calls", "length"]:
        finish_reason = "stop"
        if converse_response["stopReason"] == "tool_use":
            finish_reason = "tool_calls"
        elif converse_response["stopReason"] == "max_tokens":
            finish_reason = "length"

        return finish_reason

    @staticmethod
    def message(
        converse_response: ConverseResponseTypeDef,
        response_format: ResponseFormat | None = None,
        message_name: str | None = None,
    ) -> AssistantMessage:
        content = []
        tool_calls = []

        for block in converse_response["output"].get("message", {}).get("content", []):
            if "text" in block:
                if isinstance(response_format, JsonSchemaResponseFormat):
                    content.append(JsonContent(json=block["text"], name=response_format.json_schema.name))
                elif isinstance(response_format, JsonObjectResponseFormat):
                    content.append(JsonContent(json=block["text"], name=response_format.name))
                else:
                    content_name = response_format.name if response_format else None
                    content.append(TextContent(text=block["text"], name=content_name))

            if "toolUse" in block:
                tool_calls.append(
                    ToolCall(
                        id=block["toolUse"]["toolUseId"],
                        name=block["toolUse"]["name"],
                        arguments=json.dumps(block["toolUse"]["input"], default=str)
                        if block["toolUse"]["input"] is not None
                        else None,
                    )
                )

        return AssistantMessage(content=content, tool_calls=tool_calls, name=message_name)

    @staticmethod
    def from_converse_response(
        converse_response: ConverseResponseTypeDef,
        response_format: ResponseFormat | None = None,
        message_name: str | None = None,
    ) -> ChatCompletion:
        return ChatCompletion(
            finish_reason=ToChatCompletion.finish_reason(converse_response),
            message=ToChatCompletion.message(converse_response, response_format, message_name),
            usage=ToChatCompletion.usage(converse_response),
        )
