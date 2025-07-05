import json
import typing

from types_aiobotocore_bedrock_runtime.type_defs import ConverseResponseTypeDef

from aiomodels.chat_completions.chat_completion import ChatCompletion
from aiomodels.contents.text_content import TextContent
from aiomodels.messages.assistant_message import AssistantMessage
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
    def finish_reason(converse_response: ConverseResponseTypeDef) -> typing.Literal["stop", "tool_calls"]:
        return "tool_calls" if converse_response["stopReason"] == "tool_use" else "stop"

    @staticmethod
    def message(converse_response: ConverseResponseTypeDef, name: str | None = None) -> AssistantMessage:
        content = []
        tool_calls = []

        for block in converse_response["output"].get("message", {}).get("content", []):
            if "text" in block:
                content.append(TextContent(text=block["text"]))

            if "toolUse" in block:
                tool_calls.append(
                    ToolCall(
                        id=block["toolUse"]["toolUseId"],
                        name=block["toolUse"]["name"],
                        arguments=json.dumps(block["toolUse"]["input"], default=str)
                        if block["toolUse"]["input"]
                        else "{}",
                    )
                )

        return AssistantMessage(
            content=content,
            tool_calls=tool_calls,
            name=name,
        )

    @staticmethod
    def from_converse_response(converse_response: ConverseResponseTypeDef, name: str | None = None) -> ChatCompletion:
        return ChatCompletion(
            finish_reason=ToChatCompletion.finish_reason(converse_response),
            message=ToChatCompletion.message(converse_response, name),
            usage=ToChatCompletion.usage(converse_response),
        )
