import json
import typing

from anthropic.types.document_block_param import DocumentBlockParam
from anthropic.types.image_block_param import ImageBlockParam
from anthropic.types.message_param import MessageParam
from anthropic.types.text_block_param import TextBlockParam

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

IMAGE_MEDIA_TYPE = typing.Literal["image/png", "image/jpeg", "image/gif", "image/webp"]
DOCUMENT_MEDIA_TYPE = typing.Literal["application/pdf"]


class FromMessage:
    @staticmethod
    def from_user_content(
        content: str | TextContent | ImageContent | DocumentContent | AudioContent,
    ) -> TextBlockParam | ImageBlockParam | DocumentBlockParam:
        if isinstance(content, str):
            return {"type": "text", "text": content}

        if isinstance(content, TextContent):
            return {"type": "text", "text": content.text}

        if isinstance(content, ImageContent):
            return {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": typing.cast(IMAGE_MEDIA_TYPE, content.source.media_type),
                    "data": content.source.url.split(",")[1] if "," in content.source.url else content.source.url,
                },
            }

        if isinstance(content, DocumentContent):
            return {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": typing.cast(DOCUMENT_MEDIA_TYPE, content.source.media_type),
                    "data": content.source.url.split(",")[1] if "," in content.source.url else content.source.url,
                },
            }

        if isinstance(content, AudioContent):
            raise ValueError("Audio content not supported")

    @staticmethod
    def from_assistant_content(
        content: str | TextContent | JsonContent | RefusalContent,
    ) -> typing.Dict[str, typing.Any]:
        if isinstance(content, str):
            return {"type": "text", "text": content}

        if isinstance(content, TextContent):
            return {"type": "text", "text": content.text}

        if isinstance(content, JsonContent):
            return {"type": "text", "text": content.json}

        if isinstance(content, RefusalContent):
            return {"type": "text", "text": content.refusal}

    @staticmethod
    def from_tool_content(content: str | TextContent) -> typing.Dict[str, typing.Any]:
        if isinstance(content, str):
            return {"type": "text", "text": content}

        if isinstance(content, TextContent):
            return {"type": "text", "text": content.text}

    @staticmethod
    def from_system_content(content: str | TextContent) -> TextBlockParam:
        if isinstance(content, str):
            return {"type": "text", "text": content}

        if isinstance(content, TextContent):
            return {"type": "text", "text": content.text}

    @staticmethod
    def from_user_message(message: UserMessage) -> MessageParam:
        content = []
        if isinstance(message.content, str):
            content.append(FromMessage.from_user_content(message.content))
        else:
            content.extend([FromMessage.from_user_content(c) for c in message.content])

        return {"role": "user", "content": content}

    @staticmethod
    def from_assistant_message(message: AssistantMessage) -> MessageParam:
        content = []

        if isinstance(message.content, str):
            content.append(FromMessage.from_assistant_content(message.content))
        else:
            content.extend([FromMessage.from_assistant_content(c) for c in message.content])

        if message.tool_calls:
            for tool_call in message.tool_calls:
                content.append(
                    {
                        "type": "tool_use",
                        "id": tool_call.id,
                        "name": tool_call.name,
                        "input": json.loads(tool_call.arguments) if tool_call.arguments else {},
                    }
                )

        return {"role": "assistant", "content": content}

    @staticmethod
    def from_tool_message(message: ToolMessage) -> MessageParam:
        return {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": message.tool_result.id,
                    "content": message.tool_result.result,
                }
            ],
        }

    @staticmethod
    def from_system_message(message: SystemMessage) -> list[TextBlockParam]:
        return [FromMessage.from_system_content(message.content)]

    @staticmethod
    def from_message(message: UserMessage | AssistantMessage | ToolMessage) -> MessageParam:
        match message:
            case UserMessage():
                return FromMessage.from_user_message(message)
            case AssistantMessage():
                return FromMessage.from_assistant_message(message)
            case ToolMessage():
                return FromMessage.from_tool_message(message)

    @staticmethod
    def from_messages(messages: list[Message]) -> tuple[list[MessageParam], list[TextBlockParam]]:
        messages_param = []
        system_param = []

        for message in messages:
            if isinstance(message, SystemMessage):
                system_param.extend(FromMessage.from_system_message(message))
            else:
                messages_param.append(FromMessage.from_message(message))

        return messages_param, system_param
