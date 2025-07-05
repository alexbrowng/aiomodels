import typing

from aiomodels.chat_completion_events.chat_completion_event import ChatCompletionEvent
from aiomodels.chat_completion_events.content_delta_event import ContentDeltaEvent
from aiomodels.chat_completion_events.finish_event import FinishEvent
from aiomodels.chat_completion_events.start_event import StartEvent
from aiomodels.chat_completion_events.tool_call_event import ToolCallEvent
from aiomodels.chat_completion_events.usage_event import UsageEvent


class ChatCompletionEventHandler:
    def __init__(self, iterable: typing.AsyncIterable[ChatCompletionEvent]):
        self._iterable = iterable
        self._events: list[ChatCompletionEvent] = []

    async def on_start_event(self, event: StartEvent) -> ChatCompletionEvent | None:
        """On start event."""
        return event

    async def on_content_delta_event(self, event: ContentDeltaEvent) -> ChatCompletionEvent | None:
        """On content delta event."""
        return event

    async def on_finish_event(self, event: FinishEvent) -> ChatCompletionEvent | None:
        """On finish event."""
        return event

    async def on_tool_call_event(self, event: ToolCallEvent) -> ChatCompletionEvent | None:
        """On tool call event."""
        return event

    async def on_usage_event(self, event: UsageEvent) -> ChatCompletionEvent | None:
        """On usage event."""
        return event

    async def __aiter__(self) -> typing.AsyncIterator[ChatCompletionEvent]:
        async for original_event in self._iterable:
            match original_event:
                case StartEvent():
                    event = await self.on_start_event(original_event)
                case ContentDeltaEvent():
                    event = await self.on_content_delta_event(original_event)
                case ToolCallEvent():
                    event = await self.on_tool_call_event(original_event)
                case FinishEvent():
                    event = await self.on_finish_event(original_event)
                case UsageEvent():
                    event = await self.on_usage_event(original_event)

            if event is not None:
                self._events.append(event)
                yield event
