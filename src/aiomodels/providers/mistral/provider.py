import os
import typing

from openai import APIError

from aiomodels.chat_completion_events.chat_completion_event import ChatCompletionEvent
from aiomodels.exceptions.llm_error import LLMError
from aiomodels.messages.message import Message
from aiomodels.models.model import Model
from aiomodels.parameters.parameters import Parameters
from aiomodels.providers.openai.from_args import FromArgs
from aiomodels.providers.openai.provider import OpenAIProvider
from aiomodels.providers.openai.to_chat_completion_event import ToChatCompletionEvent
from aiomodels.response_formats.response_format import ResponseFormat
from aiomodels.tools.tool import Tool
from aiomodels.tools.tools import Tools


class MistralProvider(OpenAIProvider):
    def __init__(
        self,
        base_url: str = "https://api.mistral.ai/v1",
        api_key: str | None = os.getenv("MISTRAL_API_KEY"),
    ):
        super().__init__(base_url=base_url, api_key=api_key)

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
            stream = await self._client.chat.completions.create(**request, stream=True)
        except APIError as e:
            raise LLMError(e.message) from None

        async for event in ToChatCompletionEvent(stream=stream, model=model, name=name):
            yield event
