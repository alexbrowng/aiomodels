import typing

from openai.types.chat.chat_completion_chunk import ChatCompletionChunk, ChoiceDeltaToolCall
from openai.types.completion_usage import CompletionUsage

from aiomodels.chat_completion_events.chat_completion_event import ChatCompletionEvent
from aiomodels.chat_completion_events.chat_completion_event_factory import ChatCompletionEventFactory
from aiomodels.chat_completion_events.content_delta_event import ContentDeltaEvent
from aiomodels.chat_completion_events.finish_event import FinishEvent
from aiomodels.chat_completion_events.start_event import StartEvent
from aiomodels.chat_completion_events.tool_call_event import ToolCallEvent
from aiomodels.chat_completion_events.usage_event import UsageEvent
from aiomodels.models.model import Model


class ToChatCompletionEvent:
    def __init__(self, stream: typing.AsyncIterable[ChatCompletionChunk], model: Model, name: str | None = None):
        self._stream = stream
        self._model = model
        self._name = name
        self._tool_calls = {}

    def _start_event(self) -> StartEvent:
        return ChatCompletionEventFactory.start(model=self._model.id, name=self._name)

    def _content_delta_event(self, delta: str) -> ContentDeltaEvent:
        return ChatCompletionEventFactory.content_delta(delta=delta)

    def _finish_event(self, finish_reason: typing.Literal["stop", "tool_calls"]) -> FinishEvent:
        return ChatCompletionEventFactory.finish(finish_reason=finish_reason)

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

    def _usage_event(self, usage: CompletionUsage) -> UsageEvent:
        return ChatCompletionEventFactory.usage(
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
        )

    async def __aiter__(self) -> typing.AsyncIterator[ChatCompletionEvent]:
        yield self._start_event()

        async for chunk in self._stream:
            if chunk.usage:
                yield self._usage_event(chunk.usage)

            if not chunk.choices:
                continue

            if chunk.choices[0].delta.content:
                yield self._content_delta_event(chunk.choices[0].delta.content)

            if chunk.choices[0].delta.tool_calls:
                self._merge_tool_calls(chunk.choices[0].delta.tool_calls)

            if chunk.choices[0].finish_reason == "stop":
                yield self._finish_event(finish_reason="stop")

            if chunk.choices[0].finish_reason == "tool_calls":
                for tool_call_event in self._tool_call_events():
                    yield tool_call_event

                yield self._finish_event(finish_reason="tool_calls")
