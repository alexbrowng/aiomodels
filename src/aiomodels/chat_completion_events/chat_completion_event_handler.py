from aiomodels.chat_completion_events.chat_completion_event import ChatCompletionEvent
from aiomodels.chat_completion_events.content_delta_event import ContentDeltaEvent
from aiomodels.chat_completion_events.finish_event import FinishEvent
from aiomodels.chat_completion_events.start_event import StartEvent
from aiomodels.chat_completion_events.tool_call_event import ToolCallEvent
from aiomodels.chat_completion_events.usage_event import UsageEvent


class ChatCompletionEventHandler:
    async def on_start_event(self, event: StartEvent, events: list[ChatCompletionEvent]) -> None:
        """On start event."""

    async def on_content_delta_event(self, event: ContentDeltaEvent, events: list[ChatCompletionEvent]) -> None:
        """On content delta event."""

    async def on_finish_event(self, event: FinishEvent, events: list[ChatCompletionEvent]) -> None:
        """On finish event."""

    async def on_tool_call_event(self, event: ToolCallEvent, events: list[ChatCompletionEvent]) -> None:
        """On tool call event."""

    async def on_usage_event(self, event: UsageEvent, events: list[ChatCompletionEvent]) -> None:
        """On usage event."""

    async def __call__(self, event: ChatCompletionEvent, events: list[ChatCompletionEvent]):
        match event:
            case StartEvent():
                await self.on_start_event(event, events)
            case ContentDeltaEvent():
                await self.on_content_delta_event(event, events)
            case ToolCallEvent():
                await self.on_tool_call_event(event, events)
            case FinishEvent():
                await self.on_finish_event(event, events)
            case UsageEvent():
                await self.on_usage_event(event, events)
