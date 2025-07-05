import typing

from openai.types.chat.chat_completion import ChatCompletion as OpenAIChatCompletion

from aiomodels.chat_completions.chat_completion import ChatCompletion
from aiomodels.contents.json_content import JsonContent
from aiomodels.contents.text_content import TextContent
from aiomodels.messages.assistant_message import AssistantMessage
from aiomodels.response_formats.json_schema_response_format import JsonSchemaResponseFormat
from aiomodels.response_formats.response_format import ResponseFormat
from aiomodels.tools.tool_call import ToolCall
from aiomodels.usage.usage import Usage


class ToChatCompletion:
    @staticmethod
    def finish_reason(chat_completion: OpenAIChatCompletion) -> typing.Literal["stop", "tool_calls"]:
        return typing.cast(typing.Literal["stop", "tool_calls"], chat_completion.choices[0].finish_reason)

    @staticmethod
    def usage(chat_completion: OpenAIChatCompletion) -> Usage:
        if chat_completion.usage is None:
            return Usage(None, None, None)

        return Usage(
            chat_completion.usage.prompt_tokens,
            chat_completion.usage.completion_tokens,
            chat_completion.usage.total_tokens,
        )

    @staticmethod
    def message(
        chat_completion: OpenAIChatCompletion, response_format: ResponseFormat | None = None, name: str | None = None
    ) -> AssistantMessage:
        choice = chat_completion.choices[0]

        if not choice.message.content:
            content = []
        elif response_format and isinstance(response_format, JsonSchemaResponseFormat):
            content = [JsonContent(json=choice.message.content)]
        else:
            content = [TextContent(text=choice.message.content)]

        return AssistantMessage(
            role="assistant",
            content=content,
            tool_calls=[
                ToolCall(
                    id=tool_call.id,
                    name=tool_call.function.name,
                    arguments=tool_call.function.arguments or "{}",
                )
                for tool_call in choice.message.tool_calls or []
            ],
            name=name,
        )

    @staticmethod
    def from_chat_completion(
        chat_completion: OpenAIChatCompletion,
        response_format: ResponseFormat | None = None,
        name: str | None = None,
    ) -> ChatCompletion:
        return ChatCompletion(
            finish_reason=ToChatCompletion.finish_reason(chat_completion),
            message=ToChatCompletion.message(chat_completion, response_format, name),
            usage=ToChatCompletion.usage(chat_completion),
        )
