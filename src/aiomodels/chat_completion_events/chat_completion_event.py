import typing

from aiomodels.chat_completion_events.content_delta_event import ContentDeltaEvent
from aiomodels.chat_completion_events.content_finish_event import ContentFinishEvent
from aiomodels.chat_completion_events.content_start_event import ContentStartEvent
from aiomodels.chat_completion_events.message_finish_event import MessageFinishEvent
from aiomodels.chat_completion_events.message_start_event import MessageStartEvent
from aiomodels.chat_completion_events.message_usage_event import MessageUsageEvent
from aiomodels.chat_completion_events.tool_call_delta_event import ToolCallDeltaEvent
from aiomodels.chat_completion_events.tool_call_finish_event import ToolCallFinishEvent
from aiomodels.chat_completion_events.tool_call_start_event import ToolCallStartEvent

ChatCompletionEvent = typing.Union[
    ContentDeltaEvent,
    ContentStartEvent,
    ContentFinishEvent,
    MessageFinishEvent,
    MessageStartEvent,
    ToolCallStartEvent,
    ToolCallDeltaEvent,
    ToolCallFinishEvent,
    MessageUsageEvent,
]
