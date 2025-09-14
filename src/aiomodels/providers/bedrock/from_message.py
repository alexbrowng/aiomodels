import json
import typing

from types_aiobotocore_bedrock_runtime.type_defs import ContentBlockTypeDef, MessageTypeDef

from aiomodels.contents.audio_content import AudioContent
from aiomodels.contents.document_content import DocumentContent
from aiomodels.contents.image_content import ImageContent
from aiomodels.contents.json_content import JsonContent
from aiomodels.contents.refusal_content import RefusalContent
from aiomodels.contents.text_content import TextContent
from aiomodels.messages.assistant_message import AssistantMessage
from aiomodels.messages.message import Message
from aiomodels.messages.system_message import SystemMessage
from aiomodels.messages.tool_message import ToolMessage
from aiomodels.messages.user_message import UserMessage
from aiomodels.tools.tool import Tool
from aiomodels.tools.tool_call import ToolCall
from aiomodels.tools.tools import Tools

IMAGE_FORMAT = typing.Literal["gif", "jpeg", "png", "webp"]
FILE_FORMAT = typing.Literal["csv", "doc", "docx", "html", "md", "pdf", "txt", "xls", "xlsx"]


class FromMessage:
    @staticmethod
    def from_system_content(content: str | TextContent) -> ContentBlockTypeDef:
        if isinstance(content, str):
            return {"text": content}

        if isinstance(content, TextContent):
            return {"text": content.text}

    @staticmethod
    def from_user_content(
        content: str | TextContent | ImageContent | DocumentContent | AudioContent,
    ) -> ContentBlockTypeDef:
        if isinstance(content, str):
            return {"text": content}

        if isinstance(content, TextContent):
            return {"text": content.text}

        if isinstance(content, ImageContent):
            _type, subtype = content.source.media_type.split("/")
            return {
                "image": {
                    "format": typing.cast(IMAGE_FORMAT, subtype),
                    "source": {"bytes": content.source.bytes},
                }
            }

        if isinstance(content, DocumentContent):
            _type, subtype = content.source.media_type.split("/")
            return {
                "document": {
                    "format": typing.cast(FILE_FORMAT, subtype),
                    "name": content.name,
                    "source": {"bytes": content.source.bytes},
                }
            }

        if isinstance(content, AudioContent):
            raise NotImplementedError("Audio content is not supported")

    @staticmethod
    def from_assistant_content(
        content: str | TextContent | JsonContent | RefusalContent,
    ) -> ContentBlockTypeDef:
        if isinstance(content, str):
            return {"text": content}

        if isinstance(content, TextContent):
            return {"text": content.text}

        if isinstance(content, JsonContent):
            return {"text": content.json}

        if isinstance(content, RefusalContent):
            return {"text": content.refusal}

    @staticmethod
    def from_tool_content(content: str | TextContent) -> ContentBlockTypeDef:
        if isinstance(content, str):
            return {"text": content}

        if isinstance(content, TextContent):
            return {"text": content.text}

    @staticmethod
    def from_tool_calls(tool_calls: typing.Sequence[ToolCall]) -> list[ContentBlockTypeDef]:
        return [
            {
                "toolUse": {
                    "toolUseId": tool_call.id,
                    "name": tool_call.name,
                    "input": json.loads(tool_call.arguments) if tool_call.arguments else {},
                }
            }
            for tool_call in tool_calls
        ]

    @staticmethod
    def from_system_message(message: SystemMessage) -> ContentBlockTypeDef:
        return FromMessage.from_system_content(message.content)

    @staticmethod
    def from_user_message(message: UserMessage) -> list[MessageTypeDef]:
        messages_param: list[MessageTypeDef] = []

        content = []

        if isinstance(message.content, str):
            content.append(FromMessage.from_user_content(message.content))
        else:
            content.extend([FromMessage.from_user_content(content) for content in message.content])

        messages_param.append({"role": "user", "content": content})

        if message.tool_calls:
            messages_param.append({"role": "assistant", "content": FromMessage.from_tool_calls(message.tool_calls)})

        return messages_param

    @staticmethod
    def from_assistant_message(message: AssistantMessage) -> MessageTypeDef:
        content = []

        if message.content:
            if isinstance(message.content, str):
                content.append(FromMessage.from_assistant_content(message.content))
            else:
                content.extend([FromMessage.from_assistant_content(content) for content in message.content])

        if message.tool_calls:
            content.extend(
                [
                    {
                        "toolUse": {
                            "toolUseId": tool_call.id,
                            "name": tool_call.name,
                            "input": json.loads(tool_call.arguments) if tool_call.arguments else {},
                        },
                    }
                    for tool_call in message.tool_calls
                ]
            )

        return {"role": "assistant", "content": content}

    @staticmethod
    def from_tool_message(message: ToolMessage) -> MessageTypeDef:
        return {
            "role": "user",
            "content": [
                {
                    "toolResult": {
                        "toolUseId": message.tool_result.id,
                        "content": [{"text": message.tool_result.result}],
                    }
                }
            ],
        }

    @staticmethod
    def from_message(message: UserMessage | AssistantMessage | ToolMessage) -> MessageTypeDef | list[MessageTypeDef]:
        match message:
            case UserMessage():
                return FromMessage.from_user_message(message)
            case AssistantMessage():
                return FromMessage.from_assistant_message(message)
            case ToolMessage():
                return FromMessage.from_tool_message(message)

    @staticmethod
    def from_messages(messages: typing.Sequence[Message]) -> tuple[list[MessageTypeDef], list[ContentBlockTypeDef]]:
        messages_param = []
        system_param = []

        for message in messages:
            if isinstance(message, SystemMessage):
                system_param.extend(FromMessage.from_system_message(message))
            else:
                message_param = FromMessage.from_message(message)
                if isinstance(message_param, list):
                    messages_param.extend(message_param)
                else:
                    messages_param.append(message_param)

        return messages_param, system_param

    @staticmethod
    def from_tools(tools: Tools | typing.Sequence[Tool]) -> list[ContentBlockTypeDef]:
        system_param = []

        if isinstance(tools, Tools) and tools.instructions:
            system_param.extend(FromMessage.from_system_content(tools.instructions))

        system_param.extend(FromMessage.from_system_content(tool.instructions) for tool in tools if tool.instructions)

        return system_param
