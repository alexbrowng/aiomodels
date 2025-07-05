import typing

from aiomodels.chat_completion_events.content_delta_event import ContentDeltaEvent
from aiomodels.chat_completion_events.finish_event import FinishEvent
from aiomodels.chat_completion_events.start_event import StartEvent
from aiomodels.chat_completion_events.tool_call_event import ToolCallEvent
from aiomodels.chat_completion_events.usage_event import UsageEvent


class ChatCompletionEventFactory:
    @staticmethod
    def start(model: str, name: str | None = None) -> StartEvent:
        return StartEvent(model=model, name=name)

    @staticmethod
    def content_delta(delta: str) -> ContentDeltaEvent:
        return ContentDeltaEvent(delta=delta)

    @staticmethod
    def tool_call(id: str, name: str, arguments: str) -> ToolCallEvent:
        return ToolCallEvent(id=id, name=name, arguments=arguments)

    @staticmethod
    def finish(finish_reason: typing.Literal["stop", "tool_calls"]) -> FinishEvent:
        return FinishEvent(finish_reason=finish_reason)

    @staticmethod
    def usage(prompt_tokens: int, completion_tokens: int, total_tokens: int) -> UsageEvent:
        return UsageEvent(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens, total_tokens=total_tokens)
