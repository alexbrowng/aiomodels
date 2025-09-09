import typing

from anthropic import AsyncStream
from anthropic.types import MessageStreamEvent

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
        stream: AsyncStream[MessageStreamEvent],
        model: Model,
        content_type: ContentContentType = "text",
        name: str | None = None,
    ):
        self._stream = stream
        self._model = model
        self._content_type: ContentContentType = content_type
        self._name = name
        self._tool_calls = []

    def _message_start_event(self) -> MessageStartEvent:
        return ChatCompletionEventFactory.message_start(model=self._model.id, name=self._name)

    def _content_start_event(self, index: int, content_type: ContentContentType) -> ContentStartEvent:
        return ChatCompletionEventFactory.content_start(index=index, content_type=content_type)

    def _content_delta_event(self, index: int, delta: str) -> ContentDeltaEvent:
        return ChatCompletionEventFactory.content_delta(index=index, delta=delta)

    def _message_finish_event(self, finish_reason: typing.Literal["stop", "tool_calls"]) -> MessageFinishEvent:
        return ChatCompletionEventFactory.message_finish(reason=finish_reason)

    def _start_tool_call(self, tool_use_id: str, name: str):
        self._tool_calls.append(
            {
                "id": tool_use_id,
                "name": name,
                "arguments": "",
            }
        )

    def _merge_tool_calls(self, partial_json: str):
        if self._tool_calls:
            self._tool_calls[-1]["arguments"] += partial_json

    def _tool_call_events(self) -> typing.Sequence[ToolCallEvent]:
        return [
            ChatCompletionEventFactory.tool_call(
                id=tool_call.get("id", ""),
                name=tool_call.get("name", ""),
                arguments=tool_call.get("arguments"),
            )
            for tool_call in self._tool_calls
        ]

    def _message_usage_event(self, input_tokens: int, output_tokens: int) -> MessageUsageEvent:
        return ChatCompletionEventFactory.message_usage(
            prompt_tokens=input_tokens,
            completion_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
        )

    async def __aiter__(self) -> typing.AsyncIterator[ChatCompletionEvent]:
        yield self._message_start_event()

        input_tokens = 0
        output_tokens = 0
        index = -1

        async for event in self._stream:
            if event.type == "message_start":
                input_tokens += event.message.usage.input_tokens
                output_tokens += event.message.usage.output_tokens

            elif event.type == "content_block_start":
                if event.content_block.type == "text":
                    index += 1
                    yield self._content_start_event(index=index, content_type=self._content_type)

                if event.content_block.type == "tool_use":
                    self._start_tool_call(event.content_block.id, event.content_block.name)

            elif event.type == "content_block_delta":
                if event.delta.type == "text_delta":
                    yield self._content_delta_event(index=index, delta=event.delta.text)
                elif event.delta.type == "input_json_delta":
                    self._merge_tool_calls(event.delta.partial_json)

            elif event.type == "content_block_stop":
                continue

            elif event.type == "message_delta":
                input_tokens += event.usage.input_tokens or 0
                output_tokens += event.usage.output_tokens

            elif event.type == "message_stop":
                yield self._message_usage_event(input_tokens=input_tokens, output_tokens=output_tokens)

                if self._tool_calls:
                    for tool_call_event in self._tool_call_events():
                        yield tool_call_event

                    yield self._message_finish_event(finish_reason="tool_calls")
                else:
                    yield self._message_finish_event(finish_reason="stop")
