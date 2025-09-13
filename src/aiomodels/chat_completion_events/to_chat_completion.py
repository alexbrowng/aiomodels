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
from aiomodels.chat_completions.chat_completion import ChatCompletion
from aiomodels.contents.json_content import JsonContent
from aiomodels.contents.text_content import TextContent
from aiomodels.messages.assistant_message import AssistantMessage
from aiomodels.tools.tool_call import ToolCall
from aiomodels.usage.usage import Usage


class ToChatCompletion:
    @staticmethod
    def from_chat_completion_events(events: typing.Sequence[ChatCompletionEvent]) -> ChatCompletion:
        finish_reason = "stop"
        content: typing.Sequence[TextContent | JsonContent] = []
        tool_calls: typing.Sequence[ToolCall] = []
        usage = None

        for event in events:
            match event:
                case MessageStartEvent():
                    message_name = event.name
                case MessageFinishEvent():
                    finish_reason = event.reason
                case MessageUsageEvent():
                    usage = Usage(event.prompt_tokens, event.completion_tokens, event.total_tokens)
                case ContentStartEvent():
                    if event.content_type == "text":
                        content.append(TextContent(text=event.content or "", name=event.name, finished=False))
                    elif event.content_type == "json":
                        content.append(JsonContent(json=event.content or "", name=event.name, finished=False))
                case ContentDeltaEvent():
                    content[-1] = content[-1].delta(event.delta)
                case ContentFinishEvent():
                    content[-1] = content[-1].finish()
                case ToolCallStartEvent():
                    tool_calls.append(ToolCall(event.id, event.name, event.arguments, finished=False))
                case ToolCallDeltaEvent():
                    tool_calls[-1] = tool_calls[-1].delta(event.arguments)
                case ToolCallFinishEvent():
                    tool_calls[-1] = tool_calls[-1].finish()
                case _:
                    raise ValueError(f"Unknown event type: {type(event)}")

        message = AssistantMessage(role="assistant", content=content, tool_calls=tool_calls, name=message_name)

        return ChatCompletion(finish_reason=finish_reason, message=message, usage=usage)
