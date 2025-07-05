import typing
from typing import Generator

from openai.types.chat import ChatCompletionChunk
from openai_responses.ext.httpx import Request, Response
from openai_responses.streaming import AsyncEventStream
from typing_extensions import override


class CreateChatCompletionEventStream(AsyncEventStream[ChatCompletionChunk]):
    def __init__(self, chat_completion_chunks: typing.Sequence[dict]):
        self._chat_completion_chunks = chat_completion_chunks

    @override
    def generate(self) -> Generator[ChatCompletionChunk, None, None]:
        for chunk in self._chat_completion_chunks:
            yield ChatCompletionChunk.model_validate(chunk)


def create_chat_completion_response(
    chat_completion_chunks: typing.Sequence[dict],
) -> typing.Callable[[Request], Response]:
    def create_chat_completion_event_stream(request: Request) -> Response:
        stream = CreateChatCompletionEventStream(chat_completion_chunks)
        return Response(201, content=stream, request=request)

    return create_chat_completion_event_stream
