import typing

from openai.types.chat.chat_completion import ChatCompletion as OpenAIChatCompletion

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
    def finish_reason(chat_completion: OpenAIChatCompletion) -> typing.Literal["stop", "tool_calls", "length"]:
        finish_reason = "stop"
        if chat_completion.choices[0].finish_reason == "tool_calls":
            finish_reason = "tool_calls"
        elif chat_completion.choices[0].finish_reason == "length":
            finish_reason = "length"

        return finish_reason

    @staticmethod
    def usage(chat_completion: OpenAIChatCompletion) -> Usage | None:
        if chat_completion.usage:
            return Usage(
                chat_completion.usage.prompt_tokens,
                chat_completion.usage.completion_tokens,
                chat_completion.usage.total_tokens,
            )

    @staticmethod
    def message(
        chat_completion: OpenAIChatCompletion,
        response_format: ResponseFormat | None = None,
        message_name: str | None = None,
    ) -> AssistantMessage:
        choice = chat_completion.choices[0]

        if not choice.message.content:
            content = []
        else:
            if isinstance(response_format, JsonSchemaResponseFormat):
                content = [JsonContent(json=choice.message.content, name=response_format.json_schema.name)]
            elif isinstance(response_format, JsonObjectResponseFormat):
                content = [JsonContent(json=choice.message.content, name=response_format.name)]
            else:
                content_name = response_format.name if response_format else None
                content = [TextContent(text=choice.message.content, name=content_name)]

        tool_calls = []
        if choice.message.tool_calls:
            tool_calls = [
                ToolCall(
                    id=tool_call.id,
                    name=tool_call.function.name,
                    arguments=tool_call.function.arguments or None,
                )
                for tool_call in choice.message.tool_calls
            ]

        return AssistantMessage(role="assistant", content=content, tool_calls=tool_calls, name=message_name)

    @staticmethod
    def from_chat_completion(
        chat_completion: OpenAIChatCompletion,
        response_format: ResponseFormat | None = None,
        message_name: str | None = None,
    ) -> ChatCompletion:
        return ChatCompletion(
            finish_reason=ToChatCompletion.finish_reason(chat_completion),
            message=ToChatCompletion.message(chat_completion, response_format, message_name),
            usage=ToChatCompletion.usage(chat_completion),
        )
