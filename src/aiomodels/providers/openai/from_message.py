import json
import typing

from openai.types.chat.chat_completion_assistant_message_param import ChatCompletionAssistantMessageParam
from openai.types.chat.chat_completion_content_part_image_param import ChatCompletionContentPartImageParam, ImageURL
from openai.types.chat.chat_completion_content_part_input_audio_param import (
    ChatCompletionContentPartInputAudioParam,
    InputAudio,
)
from openai.types.chat.chat_completion_content_part_param import File, FileFile
from openai.types.chat.chat_completion_content_part_refusal_param import ChatCompletionContentPartRefusalParam
from openai.types.chat.chat_completion_content_part_text_param import ChatCompletionContentPartTextParam
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_message_tool_call_param import ChatCompletionMessageToolCallParam
from openai.types.chat.chat_completion_system_message_param import ChatCompletionSystemMessageParam
from openai.types.chat.chat_completion_tool_message_param import ChatCompletionToolMessageParam
from openai.types.chat.chat_completion_user_message_param import ChatCompletionUserMessageParam

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

AUDIO_FORMAT = typing.Literal["mp3", "wav"]


class FromMessage:
    @staticmethod
    def from_user_content(
        content: str | TextContent | ImageContent | DocumentContent | AudioContent,
    ) -> (
        ChatCompletionContentPartTextParam
        | ChatCompletionContentPartImageParam
        | ChatCompletionContentPartInputAudioParam
        | File
    ):
        if isinstance(content, str):
            return ChatCompletionContentPartTextParam(text=content, type="text")

        if isinstance(content, TextContent):
            return ChatCompletionContentPartTextParam(text=content.text, type="text")

        if isinstance(content, ImageContent):
            return ChatCompletionContentPartImageParam(
                image_url=ImageURL(url=content.source.url, detail=content.detail), type="image_url"
            )

        if isinstance(content, DocumentContent):
            return File(file=FileFile(file_data=content.source.url, filename=content.name), type="file")

        if isinstance(content, AudioContent):
            audio_format = "mp3" if content.source.media_type == "audio/mpeg" else "wav"

            return ChatCompletionContentPartInputAudioParam(
                input_audio=InputAudio(data=content.source.url, format=audio_format),
                type="input_audio",
            )

    @staticmethod
    def from_assistant_content(
        content: str | TextContent | JsonContent | RefusalContent,
    ) -> ChatCompletionContentPartTextParam | ChatCompletionContentPartRefusalParam:
        if isinstance(content, str):
            return ChatCompletionContentPartTextParam(text=content, type="text")

        if isinstance(content, TextContent):
            return ChatCompletionContentPartTextParam(text=content.text, type="text")

        if isinstance(content, JsonContent):
            return ChatCompletionContentPartTextParam(text=content.json, type="text")

        if isinstance(content, RefusalContent):
            return ChatCompletionContentPartRefusalParam(refusal=content.refusal, type="refusal")

    @staticmethod
    def from_system_content(content: str | TextContent) -> ChatCompletionContentPartTextParam:
        if isinstance(content, str):
            return ChatCompletionContentPartTextParam(text=content, type="text")

        if isinstance(content, TextContent):
            return ChatCompletionContentPartTextParam(text=content.text, type="text")

    @staticmethod
    def from_user_message(message: UserMessage) -> ChatCompletionUserMessageParam:
        content = []
        if isinstance(message.content, str):
            content.append(FromMessage.from_user_content(message.content))
        else:
            content.extend([FromMessage.from_user_content(content) for content in message.content])

        param = ChatCompletionUserMessageParam(role="user", content=content)

        if message.name:
            param["name"] = message.name

        return param

    @staticmethod
    def from_assistant_message(message: AssistantMessage) -> ChatCompletionAssistantMessageParam:
        content = []

        if isinstance(message.content, str):
            content.append(FromMessage.from_assistant_content(message.content))
        else:
            content.extend([FromMessage.from_assistant_content(content) for content in message.content])

        param = ChatCompletionAssistantMessageParam(
            role="assistant",
            content=[FromMessage.from_assistant_content(content) for content in message.content],
        )

        if len(message.tool_calls):
            param["tool_calls"] = [
                ChatCompletionMessageToolCallParam(
                    id=tool_call.id,
                    type="function",
                    function={
                        "name": tool_call.name,
                        "arguments": json.dumps(tool_call.arguments),
                    },
                )
                for tool_call in message.tool_calls
            ]

        if message.name:
            param["name"] = message.name

        return param

    @staticmethod
    def from_tool_message(message: ToolMessage) -> ChatCompletionToolMessageParam:
        return ChatCompletionToolMessageParam(
            role="tool", tool_call_id=message.tool_result.id, content=message.tool_result.result
        )

    @staticmethod
    def from_system_message(message: SystemMessage) -> ChatCompletionSystemMessageParam:
        content = [FromMessage.from_system_content(message.content)]

        param = ChatCompletionSystemMessageParam(role="system", content=content)

        return param

    @staticmethod
    def from_message(message: Message) -> ChatCompletionMessageParam:
        match message:
            case UserMessage():
                return FromMessage.from_user_message(message)
            case AssistantMessage():
                return FromMessage.from_assistant_message(message)
            case ToolMessage():
                return FromMessage.from_tool_message(message)
            case SystemMessage():
                return FromMessage.from_system_message(message)
