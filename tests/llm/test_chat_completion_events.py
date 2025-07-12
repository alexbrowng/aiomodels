from aiomodels.chat_completion_events.chat_completion_event_factory import ChatCompletionEventFactory
from aiomodels.chat_completion_events.content_delta_event import ContentDeltaEvent
from aiomodels.chat_completion_events.message_finish_event import MessageFinishEvent
from aiomodels.chat_completion_events.message_start_event import MessageStartEvent
from aiomodels.chat_completion_events.message_usage_event import MessageUsageEvent
from aiomodels.chat_completion_events.tool_call_event import ToolCallEvent


def test_start_event_creation():
    event = MessageStartEvent(model="gpt-4o-mini", name="session1")
    assert event.model == "gpt-4o-mini"
    assert event.name == "session1"
    assert event.type == "message_start"


def test_finish_event_creation():
    event = MessageFinishEvent(reason="stop")
    assert event.reason == "stop"
    assert event.type == "message_finish"


def test_content_delta_event_creation():
    event = ContentDeltaEvent(index=1, delta="Hello")
    assert event.index == 1
    assert event.delta == "Hello"
    assert event.type == "content_delta"


def test_tool_call_event_creation():
    event = ToolCallEvent(id="call1", name="get_weather", arguments='{"location": "Paris"}')
    assert event.id == "call1"
    assert event.name == "get_weather"
    assert event.arguments == '{"location": "Paris"}'
    assert event.type == "tool_call"


def test_usage_event_creation():
    event = MessageUsageEvent(prompt_tokens=10, completion_tokens=5, total_tokens=15)
    assert event.prompt_tokens == 10
    assert event.completion_tokens == 5
    assert event.total_tokens == 15
    assert event.type == "message_usage"


def test_factory_start():
    event = ChatCompletionEventFactory.message_start(model="gpt-4o-mini", name="session1")
    assert isinstance(event, MessageStartEvent)
    assert event.model == "gpt-4o-mini"
    assert event.name == "session1"


def test_factory_content_delta():
    event = ChatCompletionEventFactory.content_delta(index=1, delta="Hi!")
    assert isinstance(event, ContentDeltaEvent)
    assert event.index == 1
    assert event.delta == "Hi!"


def test_factory_tool_call():
    event = ChatCompletionEventFactory.tool_call(id="call1", name="get_weather", arguments='{"location": "Paris"}')
    assert isinstance(event, ToolCallEvent)
    assert event.id == "call1"
    assert event.name == "get_weather"
    assert event.arguments == '{"location": "Paris"}'


def test_factory_finish():
    event = ChatCompletionEventFactory.message_finish(reason="tool_calls")
    assert isinstance(event, MessageFinishEvent)
    assert event.reason == "tool_calls"


def test_factory_usage():
    event = ChatCompletionEventFactory.message_usage(prompt_tokens=1, completion_tokens=2, total_tokens=3)
    assert isinstance(event, MessageUsageEvent)
    assert event.prompt_tokens == 1
    assert event.completion_tokens == 2
    assert event.total_tokens == 3
