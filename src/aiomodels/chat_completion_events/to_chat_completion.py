import typing

from aiomodels.chat_completion_events.chat_completion_event import ChatCompletionEvent
from aiomodels.chat_completion_events.content_delta_event import ContentDeltaEvent
from aiomodels.chat_completion_events.finish_event import FinishEvent
from aiomodels.chat_completion_events.start_event import StartEvent
from aiomodels.chat_completion_events.tool_call_event import ToolCallEvent
from aiomodels.chat_completion_events.usage_event import UsageEvent
from aiomodels.chat_completions.chat_completion import ChatCompletion
from aiomodels.contents.text_content import TextContent
from aiomodels.messages.assistant_message import AssistantMessage
from aiomodels.tools.tool_call import ToolCall
from aiomodels.usage.usage import Usage


class ToChatCompletion:
    @staticmethod
    def from_chat_completion_events(events: typing.Sequence[ChatCompletionEvent]) -> ChatCompletion:
        finish_reason = None
        content = ""
        tool_calls = []
        usage = None

        for event in events:
            if isinstance(event, StartEvent):
                name = event.name

            if isinstance(event, ContentDeltaEvent):
                content += event.delta

            if isinstance(event, ToolCallEvent):
                tool_calls.append(ToolCall(event.id, event.name, event.arguments))

            if isinstance(event, FinishEvent):
                finish_reason = event.finish_reason

            if isinstance(event, UsageEvent):
                usage = Usage(event.prompt_tokens, event.completion_tokens, event.total_tokens)

        message = AssistantMessage(
            role="assistant",
            content=[TextContent(text=content)] if content else [],
            tool_calls=tool_calls,
            name=name,
        )

        return ChatCompletion(
            finish_reason=typing.cast(typing.Literal["stop", "tool_calls"], finish_reason),
            message=message,
            usage=usage,
        )
