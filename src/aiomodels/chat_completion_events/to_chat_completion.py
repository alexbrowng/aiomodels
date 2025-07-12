import typing

from aiomodels.chat_completion_events.chat_completion_event import ChatCompletionEvent
from aiomodels.chat_completion_events.content_delta_event import ContentDeltaEvent
from aiomodels.chat_completion_events.content_start_event import ContentStartEvent
from aiomodels.chat_completion_events.message_finish_event import MessageFinishEvent
from aiomodels.chat_completion_events.message_start_event import MessageStartEvent
from aiomodels.chat_completion_events.message_usage_event import MessageUsageEvent
from aiomodels.chat_completion_events.tool_call_event import ToolCallEvent
from aiomodels.chat_completions.chat_completion import ChatCompletion
from aiomodels.contents.json_content import JsonContent
from aiomodels.contents.refusal_content import RefusalContent
from aiomodels.contents.text_content import TextContent
from aiomodels.messages.assistant_message import AssistantMessage
from aiomodels.tools.tool_call import ToolCall
from aiomodels.usage.usage import Usage


class ToChatCompletion:
    @staticmethod
    def from_chat_completion_events(events: typing.Sequence[ChatCompletionEvent]) -> ChatCompletion:
        finish_reason = None
        content: list[TextContent | JsonContent | RefusalContent] = []
        tool_calls = []
        usage = None

        for event in events:
            if isinstance(event, MessageStartEvent):
                name = event.name

            if isinstance(event, ContentStartEvent):
                if event.content_type == "text":
                    content.append(TextContent(text=""))
                elif event.content_type == "json":
                    content.append(JsonContent(json=""))
                elif event.content_type == "refusal":
                    content.append(RefusalContent(refusal=""))

            if isinstance(event, ContentDeltaEvent):
                if isinstance(content[-1], TextContent):
                    content[-1] = TextContent(text=content[-1].text + event.delta)
                elif isinstance(content[-1], JsonContent):
                    content[-1] = JsonContent(json=content[-1].json + event.delta)
                elif isinstance(content[-1], RefusalContent):
                    content[-1] = RefusalContent(refusal=content[-1].refusal + event.delta)

            if isinstance(event, ToolCallEvent):
                tool_calls.append(ToolCall(event.id, event.name, event.arguments))

            if isinstance(event, MessageFinishEvent):
                finish_reason = event.reason

            if isinstance(event, MessageUsageEvent):
                usage = Usage(event.prompt_tokens, event.completion_tokens, event.total_tokens)

        message = AssistantMessage(
            role="assistant",
            content=content,
            tool_calls=tool_calls,
            name=name,
        )

        return ChatCompletion(
            finish_reason=typing.cast(typing.Literal["stop", "tool_calls"], finish_reason),
            message=message,
            usage=usage,
        )
