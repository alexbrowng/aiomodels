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


class ChatCompletionEventFactory:
    @staticmethod
    def message_start(
        model: str, role: typing.Literal["assistant", "user"] = "assistant", name: str | None = None
    ) -> MessageStartEvent:
        return MessageStartEvent(model=model, role=role, name=name)

    @staticmethod
    def content_start(
        index: int,
        content_type: typing.Literal["text", "json"],
        content: str | None = None,
        name: str | None = None,
    ) -> ContentStartEvent:
        return ContentStartEvent(index=index, content_type=content_type, content=content, name=name)

    @staticmethod
    def content_delta(index: int, delta: str) -> ContentDeltaEvent:
        return ContentDeltaEvent(index=index, delta=delta)

    @staticmethod
    def content_finish(index: int) -> ContentFinishEvent:
        return ContentFinishEvent(index=index)

    @staticmethod
    def tool_call_start(id: str, name: str, arguments: str | None) -> ToolCallStartEvent:
        return ToolCallStartEvent(id=id, name=name, arguments=arguments)

    @staticmethod
    def tool_call_delta(id: str, arguments: str) -> ToolCallDeltaEvent:
        return ToolCallDeltaEvent(id=id, arguments=arguments)

    @staticmethod
    def tool_call_finish(id: str) -> ToolCallFinishEvent:
        return ToolCallFinishEvent(id=id)

    @staticmethod
    def message_finish(reason: typing.Literal["stop", "tool_calls", "length"]) -> MessageFinishEvent:
        return MessageFinishEvent(reason=reason)

    @staticmethod
    def message_usage(prompt_tokens: int, completion_tokens: int, total_tokens: int) -> MessageUsageEvent:
        return MessageUsageEvent(
            prompt_tokens=prompt_tokens, completion_tokens=completion_tokens, total_tokens=total_tokens
        )
