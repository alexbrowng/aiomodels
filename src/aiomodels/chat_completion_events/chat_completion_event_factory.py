import typing

from aiomodels.chat_completion_events.content_delta_event import ContentDeltaEvent
from aiomodels.chat_completion_events.content_start_event import ContentStartEvent
from aiomodels.chat_completion_events.message_finish_event import MessageFinishEvent
from aiomodels.chat_completion_events.message_start_event import MessageStartEvent
from aiomodels.chat_completion_events.message_usage_event import MessageUsageEvent
from aiomodels.chat_completion_events.tool_call_event import ToolCallEvent


class ChatCompletionEventFactory:
    @staticmethod
    def message_start(
        model: str, role: typing.Literal["assistant", "user"] = "assistant", name: str | None = None
    ) -> MessageStartEvent:
        return MessageStartEvent(model=model, role=role, name=name)

    @staticmethod
    def content_start(index: int, content_type: typing.Literal["text", "json", "refusal"]) -> ContentStartEvent:
        return ContentStartEvent(index=index, content_type=content_type)

    @staticmethod
    def content_delta(index: int, delta: str) -> ContentDeltaEvent:
        return ContentDeltaEvent(index=index, delta=delta)

    @staticmethod
    def tool_call(id: str, name: str, arguments: str) -> ToolCallEvent:
        return ToolCallEvent(id=id, name=name, arguments=arguments)

    @staticmethod
    def message_finish(reason: typing.Literal["stop", "tool_calls"]) -> MessageFinishEvent:
        return MessageFinishEvent(reason=reason)

    @staticmethod
    def message_usage(prompt_tokens: int, completion_tokens: int, total_tokens: int) -> MessageUsageEvent:
        return MessageUsageEvent(
            prompt_tokens=prompt_tokens, completion_tokens=completion_tokens, total_tokens=total_tokens
        )
