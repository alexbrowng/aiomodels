import typing

from aiomodels.chat_completion_events.chat_completion_event import ChatCompletionEvent
from aiomodels.chat_completion_events.content_delta_event import ContentDeltaEvent
from aiomodels.chat_completion_events.content_finish_event import ContentFinishEvent
from aiomodels.chat_completion_events.content_start_event import ContentStartEvent
from aiomodels.chat_completion_events.message_finish_event import MessageFinishEvent
from aiomodels.chat_completion_events.message_start_event import MessageStartEvent
from aiomodels.chat_completion_events.message_usage_event import MessageUsageEvent
from aiomodels.chat_completion_events.tool_call_delta_event import ToolCallDeltaEvent
from aiomodels.chat_completion_events.tool_call_finish_event import ToolCallFinishEvent
from aiomodels.chat_completion_events.tool_call_start_event import ToolCallStartEvent


class ChatCompletionEventIterator:
    def __init__(self, iterable: typing.AsyncIterable[ChatCompletionEvent]):
        self._iterable = iterable
        self._events: list[ChatCompletionEvent] = []

    async def on_message_start_event(
        self, event: MessageStartEvent
    ) -> ChatCompletionEvent | list[ChatCompletionEvent] | None:
        """On start event."""
        return event

    async def on_content_start_event(
        self, event: ContentStartEvent
    ) -> ChatCompletionEvent | list[ChatCompletionEvent] | None:
        """On content start event."""
        return event

    async def on_content_delta_event(
        self, event: ContentDeltaEvent
    ) -> ChatCompletionEvent | list[ChatCompletionEvent] | None:
        """On content delta event."""
        return event

    async def on_content_finish_event(
        self, event: ContentFinishEvent
    ) -> ChatCompletionEvent | list[ChatCompletionEvent] | None:
        """On content finish event."""
        return event

    async def on_message_finish_event(
        self, event: MessageFinishEvent
    ) -> ChatCompletionEvent | list[ChatCompletionEvent] | None:
        """On finish event."""
        return event

    async def on_tool_call_start_event(
        self, event: ToolCallStartEvent
    ) -> ChatCompletionEvent | list[ChatCompletionEvent] | None:
        """On tool call start event."""
        return event

    async def on_tool_call_delta_event(
        self, event: ToolCallDeltaEvent
    ) -> ChatCompletionEvent | list[ChatCompletionEvent] | None:
        """On tool call delta event."""
        return event

    async def on_tool_call_finish_event(
        self, event: ToolCallFinishEvent
    ) -> ChatCompletionEvent | list[ChatCompletionEvent] | None:
        """On tool call finish event."""
        return event

    async def on_message_usage_event(
        self, event: MessageUsageEvent
    ) -> ChatCompletionEvent | list[ChatCompletionEvent] | None:
        """On usage event."""
        return event

    async def __aiter__(self) -> typing.AsyncIterator[ChatCompletionEvent]:
        async for original_event in self._iterable:
            match original_event:
                case MessageStartEvent():
                    events = await self.on_message_start_event(original_event)
                case ContentStartEvent():
                    events = await self.on_content_start_event(original_event)
                case ContentDeltaEvent():
                    events = await self.on_content_delta_event(original_event)
                case ContentFinishEvent():
                    events = await self.on_content_finish_event(original_event)
                case ToolCallStartEvent():
                    events = await self.on_tool_call_start_event(original_event)
                case ToolCallDeltaEvent():
                    events = await self.on_tool_call_delta_event(original_event)
                case ToolCallFinishEvent():
                    events = await self.on_tool_call_finish_event(original_event)
                case MessageFinishEvent():
                    events = await self.on_message_finish_event(original_event)
                case MessageUsageEvent():
                    events = await self.on_message_usage_event(original_event)

            events = events or []
            events = events if isinstance(events, list) else [events]
            self._events.extend(events)

            for event in events:
                yield event
