import os
import typing

import aioboto3

from aiomodels.chat_completion_events.chat_completion_event import ChatCompletionEvent
from aiomodels.chat_completions.chat_completion import ChatCompletion
from aiomodels.exceptions.llm_error import LLMError
from aiomodels.messages.message import Message
from aiomodels.models.model import Model
from aiomodels.parameters.parameters import Parameters
from aiomodels.providers.bedrock.from_args import FromArgs
from aiomodels.providers.bedrock.to_chat_completion import ToChatCompletion
from aiomodels.providers.bedrock.to_chat_completion_event import ToChatCompletionEvent
from aiomodels.providers.provider import Provider
from aiomodels.response_formats.response_format import ResponseFormat
from aiomodels.tools.tool import Tool
from aiomodels.tools.tools import Tools


class BedrockProvider(Provider):
    def __init__(
        self,
        region_name: str | None = os.getenv("AWS_REGION"),
        access_key_id: str | None = os.getenv("AWS_ACCESS_KEY_ID"),
        secret_access_key: str | None = os.getenv("AWS_SECRET_ACCESS_KEY"),
    ):
        self._region_name = region_name
        self._access_key_id = access_key_id
        self._secret_access_key = secret_access_key

    @property
    def session(self) -> aioboto3.Session:
        return aioboto3.Session(
            region_name=self._region_name,
            aws_access_key_id=self._access_key_id,
            aws_secret_access_key=self._secret_access_key,
        )

    async def chat_completion(
        self,
        model: Model,
        messages: typing.Sequence[Message],
        tools: Tools | typing.Sequence[Tool] | None = None,
        response_format: ResponseFormat | None = None,
        parameters: Parameters | None = None,
        name: str | None = None,
    ) -> ChatCompletion:
        async with self.session.client("bedrock-runtime") as client:
            request = FromArgs.from_args(
                model_id=model.id,
                messages=messages,
                tools=tools,
                parameters=parameters,
                response_format=response_format,
            )
            try:
                response = await client.converse(**request)
            except Exception as e:
                raise LLMError(e) from None
            return ToChatCompletion.from_converse_response(response, name)

    async def chat_completion_stream(
        self,
        model: Model,
        messages: typing.Sequence[Message],
        tools: Tools | typing.Sequence[Tool] | None = None,
        response_format: ResponseFormat | None = None,
        parameters: Parameters | None = None,
        name: str | None = None,
    ) -> typing.AsyncIterator[ChatCompletionEvent]:
        async with self.session.client("bedrock-runtime") as client:
            request = FromArgs.from_args(
                model_id=model.id,
                messages=messages,
                tools=tools,
                parameters=parameters,
                response_format=response_format,
            )

            response = await client.converse_stream(**request)

            async for event in ToChatCompletionEvent(response=response, model=model, name=name):
                yield event
