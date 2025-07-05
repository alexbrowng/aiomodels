from aiomodels.chat_completion_events.chat_completion_event_factory import ChatCompletionEventFactory
from aiomodels.chat_completion_events.content_delta_event import ContentDeltaEvent
from aiomodels.chat_completion_events.finish_event import FinishEvent
from aiomodels.chat_completion_events.start_event import StartEvent
from aiomodels.chat_completion_events.tool_call_event import ToolCallEvent
from aiomodels.chat_completion_events.usage_event import UsageEvent


def test_start_event_creation():
    event = StartEvent(model="gpt-4o-mini", name="session1")
    assert event.model == "gpt-4o-mini"
    assert event.name == "session1"
    assert event.type == "start"


def test_finish_event_creation():
    event = FinishEvent(finish_reason="stop")
    assert event.finish_reason == "stop"
    assert event.type == "finish"


def test_content_delta_event_creation():
    event = ContentDeltaEvent(delta="Hello")
    assert event.delta == "Hello"
    assert event.type == "content_delta"


def test_tool_call_event_creation():
    event = ToolCallEvent(id="call1", name="get_weather", arguments={"location": "Paris"})
    assert event.id == "call1"
    assert event.name == "get_weather"
    assert event.arguments == {"location": "Paris"}
    assert event.type == "tool_call"


def test_usage_event_creation():
    event = UsageEvent(prompt_tokens=10, completion_tokens=5, total_tokens=15)
    assert event.prompt_tokens == 10
    assert event.completion_tokens == 5
    assert event.total_tokens == 15
    assert event.type == "usage"


def test_factory_start():
    event = ChatCompletionEventFactory.start(model="gpt-4o-mini", name="session1")
    assert isinstance(event, StartEvent)
    assert event.model == "gpt-4o-mini"
    assert event.name == "session1"


def test_factory_content_delta():
    event = ChatCompletionEventFactory.content_delta(delta="Hi!")
    assert isinstance(event, ContentDeltaEvent)
    assert event.delta == "Hi!"


def test_factory_tool_call():
    event = ChatCompletionEventFactory.tool_call(id="call1", name="get_weather", arguments={"location": "Paris"})
    assert isinstance(event, ToolCallEvent)
    assert event.id == "call1"
    assert event.name == "get_weather"
    assert event.arguments == {"location": "Paris"}


def test_factory_finish():
    event = ChatCompletionEventFactory.finish(finish_reason="tool_calls")
    assert isinstance(event, FinishEvent)
    assert event.finish_reason == "tool_calls"


def test_factory_usage():
    event = ChatCompletionEventFactory.usage(prompt_tokens=1, completion_tokens=2, total_tokens=3)
    assert isinstance(event, UsageEvent)
    assert event.prompt_tokens == 1
    assert event.completion_tokens == 2
    assert event.total_tokens == 3
