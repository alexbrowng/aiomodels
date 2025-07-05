import pytest
from aiomodels.chat_completion_events.content_delta_event import ContentDeltaEvent
from aiomodels.chat_completion_events.finish_event import FinishEvent
from aiomodels.chat_completion_events.start_event import StartEvent
from aiomodels.chat_completion_events.to_chat_completion import ToChatCompletion
from aiomodels.chat_completion_events.tool_call_event import ToolCallEvent
from aiomodels.chat_completion_events.usage_event import UsageEvent
from aiomodels.chat_completions.chat_completion import ChatCompletion
from aiomodels.contents.text_content import TextContent
from aiomodels.tools.tool_call import ToolCall


def test_from_chat_completion_events_text_only():
    events = [
        StartEvent(model="gpt-4o-mini"),
        ContentDeltaEvent(delta="Hello "),
        ContentDeltaEvent(delta="world!"),
        FinishEvent(finish_reason="stop"),
        UsageEvent(prompt_tokens=1, completion_tokens=2, total_tokens=3),
    ]
    chat = ToChatCompletion.from_chat_completion_events(events)
    assert isinstance(chat, ChatCompletion)
    assert len(chat.message.content) == 1
    assert isinstance(chat.message.content[0], TextContent)
    assert chat.message.content[0].text == "Hello world!"
    assert chat.finish_reason == "stop"
    assert chat.usage is not None
    assert chat.usage.prompt_tokens == 1
    assert chat.usage.completion_tokens == 2
    assert chat.usage.total_tokens == 3
    assert chat.message.tool_calls == []
    assert chat.message.name is None


def test_from_chat_completion_events_with_tool_call():
    events = [
        StartEvent(model="gpt-4o-mini"),
        ToolCallEvent(id="call1", name="get_weather", arguments={"location": "Paris"}),
        FinishEvent(finish_reason="tool_calls"),
        UsageEvent(prompt_tokens=2, completion_tokens=3, total_tokens=5),
    ]
    chat = ToChatCompletion.from_chat_completion_events(events)
    assert chat.finish_reason == "tool_calls"
    assert len(chat.message.tool_calls) == 1
    tool_call = chat.message.tool_calls[0]
    assert isinstance(tool_call, ToolCall)
    assert tool_call.id == "call1"
    assert tool_call.name == "get_weather"
    assert tool_call.arguments == {"location": "Paris"}
    assert chat.message.content == []


def test_from_chat_completion_events_full_sequence():
    events = [
        StartEvent(model="gpt-4o-mini", name="asst1"),
        ContentDeltaEvent(delta="Hi "),
        ContentDeltaEvent(delta="there!"),
        ToolCallEvent(id="call2", name="get_time", arguments={}),
        FinishEvent(finish_reason="stop"),
        UsageEvent(prompt_tokens=5, completion_tokens=6, total_tokens=11),
    ]
    chat = ToChatCompletion.from_chat_completion_events(events)
    assert chat.message.name == "asst1"
    assert len(chat.message.content) == 1
    assert isinstance(chat.message.content[0], TextContent)
    assert chat.message.content[0].text == "Hi there!"
    assert len(chat.message.tool_calls) == 1
    assert chat.message.tool_calls[0].id == "call2"
    assert chat.finish_reason == "stop"
    assert chat.usage is not None
    assert chat.usage.total_tokens == 11


def test_from_chat_completion_events_missing_usage():
    events = [
        StartEvent(model="gpt-4o-mini"),
        ContentDeltaEvent(delta="Hi!"),
        FinishEvent(finish_reason="stop"),
    ]

    chat_completion = ToChatCompletion.from_chat_completion_events(events)
    assert chat_completion.usage is None


@pytest.mark.xfail(reason="TODO: fix this")
def test_from_chat_completion_events_missing_finish():
    events = [
        StartEvent(model="gpt-4o-mini"),
        ContentDeltaEvent(delta="Hi!"),
        UsageEvent(prompt_tokens=1, completion_tokens=2, total_tokens=3),
    ]
    with pytest.raises(Exception):
        ToChatCompletion.from_chat_completion_events(events)


def test_from_chat_completion_events_with_and_without_name():
    events_with_name = [
        StartEvent(model="gpt-4o-mini", name="asst2"),
        ContentDeltaEvent(delta="Hello!"),
        FinishEvent(finish_reason="stop"),
        UsageEvent(prompt_tokens=1, completion_tokens=2, total_tokens=3),
    ]
    chat = ToChatCompletion.from_chat_completion_events(events_with_name)
    assert chat.message.name == "asst2"

    events_without_name = [
        StartEvent(model="gpt-4o-mini"),
        ContentDeltaEvent(delta="Hello!"),
        FinishEvent(finish_reason="stop"),
        UsageEvent(prompt_tokens=1, completion_tokens=2, total_tokens=3),
    ]
    chat = ToChatCompletion.from_chat_completion_events(events_without_name)
    assert chat.message.name is None
