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


class ChatCompletionEventHandler:
    async def on_message_start_event(self, event: MessageStartEvent, events: list[ChatCompletionEvent]) -> None:
        """On start event."""

    async def on_content_start_event(self, event: ContentStartEvent, events: list[ChatCompletionEvent]) -> None:
        """On content start event."""

    async def on_content_delta_event(self, event: ContentDeltaEvent, events: list[ChatCompletionEvent]) -> None:
        """On content delta event."""

    async def on_content_finish_event(self, event: ContentFinishEvent, events: list[ChatCompletionEvent]) -> None:
        """On content finish event."""

    async def on_message_finish_event(self, event: MessageFinishEvent, events: list[ChatCompletionEvent]) -> None:
        """On finish event."""

    async def on_tool_call_start_event(self, event: ToolCallStartEvent, events: list[ChatCompletionEvent]) -> None:
        """On tool call start event."""

    async def on_tool_call_delta_event(self, event: ToolCallDeltaEvent, events: list[ChatCompletionEvent]) -> None:
        """On tool call delta event."""

    async def on_tool_call_finish_event(self, event: ToolCallFinishEvent, events: list[ChatCompletionEvent]) -> None:
        """On tool call end event."""

    async def on_message_usage_event(self, event: MessageUsageEvent, events: list[ChatCompletionEvent]) -> None:
        """On usage event."""

    async def __call__(self, event: ChatCompletionEvent, events: list[ChatCompletionEvent]):
        match event:
            case MessageStartEvent():
                await self.on_message_start_event(event, events)
            case ContentStartEvent():
                await self.on_content_start_event(event, events)
            case ContentDeltaEvent():
                await self.on_content_delta_event(event, events)
            case ContentFinishEvent():
                await self.on_content_finish_event(event, events)
            case ToolCallStartEvent():
                await self.on_tool_call_start_event(event, events)
            case ToolCallDeltaEvent():
                await self.on_tool_call_delta_event(event, events)
            case ToolCallFinishEvent():
                await self.on_tool_call_finish_event(event, events)
            case MessageFinishEvent():
                await self.on_message_finish_event(event, events)
            case MessageUsageEvent():
                await self.on_message_usage_event(event, events)
