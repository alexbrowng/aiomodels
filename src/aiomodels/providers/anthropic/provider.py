import os
import typing

from anthropic import APIError, AsyncAnthropic

from aiomodels.chat_completion_events.chat_completion_event import ChatCompletionEvent
from aiomodels.chat_completions.chat_completion import ChatCompletion
from aiomodels.exceptions.llm_error import LLMError
from aiomodels.messages.message import Message
from aiomodels.models.model import Model
from aiomodels.parameters.parameters import Parameters
from aiomodels.providers.anthropic.from_args import FromArgs
from aiomodels.providers.anthropic.to_chat_completion import ToChatCompletion
from aiomodels.providers.anthropic.to_chat_completion_event import ToChatCompletionEvent
from aiomodels.providers.provider import Provider
from aiomodels.response_formats.response_format import ResponseFormat
from aiomodels.tools.tool import Tool
from aiomodels.tools.tools import Tools


class AnthropicProvider(Provider):
    def __init__(
        self,
        base_url: str = "https://api.anthropic.com",
        api_key: str | None = os.getenv("ANTHROPIC_API_KEY"),
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url
        self._client = AsyncAnthropic(api_key=self._api_key, base_url=self._base_url)

    async def chat_completion(
        self,
        model: Model,
        messages: list[Message],
        tools: Tools | list[Tool] | None = None,
        response_format: ResponseFormat | None = None,
        parameters: Parameters | None = None,
        name: str | None = None,
    ) -> ChatCompletion:
        request = FromArgs.from_args(
            model=model.id,
            messages=messages,
            tools=tools,
            parameters=parameters,
            response_format=response_format,
        )

        try:
            message = await self._client.messages.create(**request)
        except APIError as e:
            raise LLMError(str(e)) from None

        return ToChatCompletion.from_message(message, response_format, name)

    async def chat_completion_stream(
        self,
        model: Model,
        messages: list[Message],
        tools: Tools | list[Tool] | None = None,
        response_format: ResponseFormat | None = None,
        parameters: Parameters | None = None,
        name: str | None = None,
    ) -> typing.AsyncIterator[ChatCompletionEvent]:
        request = FromArgs.from_args(
            model=model.id,
            messages=messages,
            tools=tools,
            parameters=parameters,
            response_format=response_format,
        )

        try:
            stream = await self._client.messages.create(**request, stream=True)
        except APIError as e:
            raise LLMError(str(e)) from None

        content_type = self.response_format_content_type(response_format)
        content_name = self.response_format_content_name(response_format)

        async for event in ToChatCompletionEvent(
            stream=stream,
            model=model,
            content_type=content_type,
            content_name=content_name,
            message_name=name,
        ):
            yield event
