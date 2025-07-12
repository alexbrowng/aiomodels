import typing

from openai.types.chat.chat_completion_chunk import ChatCompletionChunk, ChoiceDeltaToolCall
from openai.types.completion_usage import CompletionUsage

from aiomodels.chat_completion_events.chat_completion_event import ChatCompletionEvent
from aiomodels.chat_completion_events.chat_completion_event_factory import ChatCompletionEventFactory
from aiomodels.chat_completion_events.content_delta_event import ContentDeltaEvent
from aiomodels.chat_completion_events.content_start_event import ContentStartEvent
from aiomodels.chat_completion_events.message_finish_event import MessageFinishEvent
from aiomodels.chat_completion_events.message_start_event import MessageStartEvent
from aiomodels.chat_completion_events.message_usage_event import MessageUsageEvent
from aiomodels.chat_completion_events.tool_call_event import ToolCallEvent
from aiomodels.models.model import Model

ContentContentType = typing.Literal["text", "json", "refusal"]


class ToChatCompletionEvent:
    def __init__(
        self,
        stream: typing.AsyncIterable[ChatCompletionChunk],
        model: Model,
        content_type: ContentContentType = "text",
        name: str | None = None,
    ):
        self._stream = stream
        self._model = model
        self._content_type: ContentContentType = content_type
        self._name = name
        self._tool_calls = {}

    def _message_start_event(self) -> MessageStartEvent:
        return ChatCompletionEventFactory.message_start(model=self._model.id, name=self._name)

    def _content_start_event(self, index: int, content_type: ContentContentType) -> ContentStartEvent:
        return ChatCompletionEventFactory.content_start(index=index, content_type=content_type)

    def _content_delta_event(
        self,
        index: int,
        delta: str,
    ) -> ContentDeltaEvent:
        return ChatCompletionEventFactory.content_delta(index=index, delta=delta)

    def _message_finish_event(self, reason: typing.Literal["stop", "tool_calls"]) -> MessageFinishEvent:
        return ChatCompletionEventFactory.message_finish(reason=reason)

    def _merge_tool_calls(self, tool_calls: typing.Sequence[ChoiceDeltaToolCall]):
        for tool_call in tool_calls:
            if tool_call.id:
                self._tool_calls.setdefault(tool_call.index, {}).setdefault("id", tool_call.id)

            if tool_call.function and tool_call.function.name:
                self._tool_calls.setdefault(tool_call.index, {}).setdefault("name", tool_call.function.name)

            if tool_call.function and tool_call.function.arguments:
                self._tool_calls.setdefault(tool_call.index, {}).setdefault("arguments", "")
                self._tool_calls[tool_call.index]["arguments"] += tool_call.function.arguments

    def _tool_call_events(self) -> typing.Sequence[ToolCallEvent]:
        return [
            ChatCompletionEventFactory.tool_call(
                id=tool_call.get("id", ""),
                name=tool_call.get("name", ""),
                arguments=tool_call.get("arguments") or "{}",
            )
            for tool_call in self._tool_calls.values()
        ]

    def _message_usage_event(self, usage: CompletionUsage) -> MessageUsageEvent:
        return ChatCompletionEventFactory.message_usage(
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
        )

    async def __aiter__(self) -> typing.AsyncIterator[ChatCompletionEvent]:
        index = -1

        yield self._message_start_event()

        async for chunk in self._stream:
            if chunk.usage:
                yield self._message_usage_event(chunk.usage)

            if not chunk.choices:
                continue

            if chunk.choices[0].delta.content:
                if index == -1:
                    index += 1
                    yield self._content_start_event(index=index, content_type=self._content_type)

                yield self._content_delta_event(index=index, delta=chunk.choices[0].delta.content)

            if chunk.choices[0].delta.tool_calls:
                self._merge_tool_calls(chunk.choices[0].delta.tool_calls)

            if chunk.choices[0].finish_reason == "stop":
                yield self._message_finish_event(reason="stop")

            if chunk.choices[0].finish_reason == "tool_calls":
                for tool_call_event in self._tool_call_events():
                    yield tool_call_event

                yield self._message_finish_event(reason="tool_calls")
