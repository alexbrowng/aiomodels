import abc
import typing

from aiomodels.chat_completion_events.chat_completion_event import ChatCompletionEvent
from aiomodels.chat_completions.chat_completion import ChatCompletion
from aiomodels.messages.message import Message
from aiomodels.models.model import Model
from aiomodels.parameters.parameters import Parameters
from aiomodels.response_formats.json_object_response_format import JsonObjectResponseFormat
from aiomodels.response_formats.json_schema_response_format import JsonSchemaResponseFormat
from aiomodels.response_formats.response_format import ResponseFormat
from aiomodels.tools.tool import Tool
from aiomodels.tools.tools import Tools


class Provider(abc.ABC):
    def response_format_content_type(self, response_format: ResponseFormat | None) -> typing.Literal["text", "json"]:
        is_json_schema = isinstance(response_format, JsonSchemaResponseFormat)
        is_json_object = isinstance(response_format, JsonObjectResponseFormat)
        return "json" if is_json_schema or is_json_object else "text"

    @abc.abstractmethod
    def chat_completion(
        self,
        model: Model,
        messages: typing.Sequence[Message],
        tools: Tools | typing.Sequence[Tool] | None = None,
        response_format: ResponseFormat | None = None,
        parameters: Parameters | None = None,
        name: str | None = None,
    ) -> typing.Awaitable[ChatCompletion]:
        """
        Returns the chat completion.
        """

    @abc.abstractmethod
    def chat_completion_stream(
        self,
        model: Model,
        messages: typing.Sequence[Message],
        tools: Tools | typing.Sequence[Tool] | None = None,
        response_format: ResponseFormat | None = None,
        parameters: Parameters | None = None,
        name: str | None = None,
    ) -> typing.AsyncIterator[ChatCompletionEvent]:
        """
        Streams the chat completion events.
        """
