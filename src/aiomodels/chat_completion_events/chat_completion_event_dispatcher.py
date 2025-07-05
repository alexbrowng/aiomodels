from aiomodels.chat_completion_events.chat_completion_event import ChatCompletionEvent
from aiomodels.chat_completion_events.chat_completion_event_handler import ChatCompletionEventHandler


class ChatCompletionEventDispatcher:
    def __init__(self, event_handlers: list[ChatCompletionEventHandler]):
        self._event_handlers = event_handlers

    async def __call__(self, event: ChatCompletionEvent, events: list[ChatCompletionEvent]):
        for event_handler in self._event_handlers:
            await event_handler(event, events)
