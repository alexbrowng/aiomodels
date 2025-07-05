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
from aiomodels.messages.system_message import SystemMessage
from aiomodels.messages.tool_message import ToolMessage
from aiomodels.messages.user_message import UserMessage

IMAGE_FORMAT = typing.Literal["gif", "jpeg", "png", "webp"]
FILE_FORMAT = typing.Literal["csv", "doc", "docx", "html", "md", "pdf", "txt", "xls", "xlsx"]


class FromMessage:
    @staticmethod
    def from_system_message(message: SystemMessage) -> ContentBlockTypeDef:
        return {"text": message.content}

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
    def from_user_message(message: UserMessage) -> MessageTypeDef:
        content = []

        if isinstance(message.content, str):
            content.append(FromMessage.from_user_content(message.content))
        else:
            content.extend([FromMessage.from_user_content(content) for content in message.content])

        return {"role": "user", "content": content}

    @staticmethod
    def from_assistant_content(content: str | TextContent | JsonContent | RefusalContent) -> ContentBlockTypeDef:
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
    def from_message(message: UserMessage | AssistantMessage | ToolMessage) -> MessageTypeDef:
        match message:
            case UserMessage():
                return FromMessage.from_user_message(message)
            case AssistantMessage():
                return FromMessage.from_assistant_message(message)
            case ToolMessage():
                return FromMessage.from_tool_message(message)
