import os
import typing

from openai import APIError, AsyncOpenAI

from aiomodels.chat_completion_events.chat_completion_event import ChatCompletionEvent
from aiomodels.chat_completions.chat_completion import ChatCompletion
from aiomodels.exceptions.llm_error import LLMError
from aiomodels.messages.message import Message
from aiomodels.models.model import Model
from aiomodels.parameters.parameters import Parameters
from aiomodels.providers.openai.from_args import FromArgs
from aiomodels.providers.openai.to_chat_completion import ToChatCompletion
from aiomodels.providers.openai.to_chat_completion_event import ToChatCompletionEvent
from aiomodels.providers.provider import Provider
from aiomodels.response_formats.response_format import ResponseFormat
from aiomodels.tools.tool import Tool
from aiomodels.tools.tools import Tools


class OpenAIProvider(Provider):
    def __init__(
        self, base_url: str = "https://api.openai.com/v1", api_key: str | None = os.getenv("OPENAI_API_KEY")
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url
        self._client = AsyncOpenAI(api_key=self._api_key, base_url=self._base_url)

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
            chat_completion = await self._client.chat.completions.create(**request)
        except APIError as e:
            raise LLMError(e.message) from None

        return ToChatCompletion.from_chat_completion(chat_completion, response_format, name)

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
            stream = await self._client.chat.completions.create(
                **request,
                stream=True,
                stream_options={"include_usage": True},
            )
        except APIError as e:
            raise LLMError(e.message) from None

        async for event in ToChatCompletionEvent(stream=stream, model=model, name=name):
            yield event
