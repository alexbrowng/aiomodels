import openai_responses
import pytest

from aiomodels.chat_completion_events.content_delta_event import ContentDeltaEvent
from aiomodels.chat_completion_events.to_chat_completion import ToChatCompletion
from aiomodels.contents.text_content import TextContent
from aiomodels.messages.system_message import SystemMessage
from aiomodels.messages.user_message import UserMessage
from aiomodels.models.model import Model
from aiomodels.providers.openai.provider import OpenAIProvider
from tests.openai.chat_completion_chunks.get_weather import GET_WEATHER_CHAT_COMPLETION_CHUNKS
from tests.openai.chat_completion_chunks.hello import HELLO_CHAT_COMPLETION_CHUNKS
from tests.openai.create_chat_completion_response import create_chat_completion_response


@pytest.mark.asyncio
@openai_responses.mock()
async def test_async_create_chat_completion_stream(openai_mock: openai_responses.OpenAIMock):
    openai_mock.chat.completions.create.response = create_chat_completion_response(HELLO_CHAT_COMPLETION_CHUNKS)

    provider = OpenAIProvider(api_key="sk-fake123")
    model = Model(id="gpt-4.1-nano-2025-04-14", name="GPT 4.1 nano", provider="OpenAI")
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content=[TextContent(text="Hello!")]),
    ]

    events = []
    async for event in provider.chat_completion_stream(model=model, messages=messages):
        events.append(event)

    start = events[0]
    assert start.type == "message_start"
    assert start.model == "gpt-4.1-nano-2025-04-14"
    assert start.name is None

    content_deltas = [event.delta for event in events[1:-2] if isinstance(event, ContentDeltaEvent)]
    assert "".join(content_deltas) == "Hello! How can I assist you today?"

    finish = events[-2]
    assert finish.type == "message_finish"

    usage = events[-1]
    assert usage.type == "message_usage"
    assert usage.prompt_tokens == 19
    assert usage.completion_tokens == 10
    assert usage.total_tokens == 29


@pytest.mark.asyncio
@openai_responses.mock()
async def test_async_create_chat_completion_stream_to_chat_completion(openai_mock: openai_responses.OpenAIMock):
    openai_mock.chat.completions.create.response = create_chat_completion_response(HELLO_CHAT_COMPLETION_CHUNKS)

    provider = OpenAIProvider(api_key="sk-fake123")
    model = Model(id="gpt-4.1-nano-2025-04-14", name="GPT 4.1 nano", provider="OpenAI")
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content=[TextContent(text="Hello!")]),
    ]

    events = []
    async for event in provider.chat_completion_stream(model=model, messages=messages):
        events.append(event)

    chat_completion = ToChatCompletion.from_chat_completion_events(events)

    assert len(chat_completion.message.content) == 1
    assert isinstance(chat_completion.message.content[0], TextContent)
    assert chat_completion.message.content[0].text == "Hello! How can I assist you today?"
    assert chat_completion.message.name is None
    assert chat_completion.message.role == "assistant"
    assert chat_completion.message.tool_calls == []
    assert chat_completion.usage is not None
    assert chat_completion.usage.prompt_tokens == 19
    assert chat_completion.usage.completion_tokens == 10
    assert chat_completion.usage.total_tokens == 29


@pytest.mark.asyncio
@openai_responses.mock()
async def test_async_create_chat_completion_stream_with_tools(openai_mock: openai_responses.OpenAIMock):
    openai_mock.chat.completions.create.response = create_chat_completion_response(GET_WEATHER_CHAT_COMPLETION_CHUNKS)

    provider = OpenAIProvider(api_key="sk-fake123")
    model = Model(id="gpt-4.1-nano-2025-04-14", name="GPT 4.1 nano", provider="OpenAI")
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content=[TextContent(text="What is the weather in Tokyo?")]),
    ]

    events = []
    async for event in provider.chat_completion_stream(model=model, messages=messages):
        events.append(event)

    start = events[0]
    assert start.type == "message_start"
    assert start.model == "gpt-4.1-nano-2025-04-14"
    assert start.name is None

    tool_calls = events[1]
    assert tool_calls.type == "tool_call"
    assert tool_calls.id == "call_PieqNSej6kM9hgYbcQdbZSaC"
    assert tool_calls.name == "get_weather"
    assert tool_calls.arguments == '{"location": "Tokyo"}'

    finish = events[-2]
    assert finish.type == "message_finish"

    usage = events[-1]
    assert usage.type == "message_usage"
    assert usage.prompt_tokens == 67
    assert usage.completion_tokens == 31
    assert usage.total_tokens == 98


@pytest.mark.asyncio
@openai_responses.mock()
async def test_async_create_chat_completion_stream_with_tools_to_chat_completion(
    openai_mock: openai_responses.OpenAIMock,
):
    openai_mock.chat.completions.create.response = create_chat_completion_response(GET_WEATHER_CHAT_COMPLETION_CHUNKS)

    provider = OpenAIProvider(api_key="sk-fake123")
    model = Model(id="gpt-4.1-nano-2025-04-14", name="GPT 4.1 nano", provider="OpenAI")
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content=[TextContent(text="What is the weather in Tokyo?")]),
    ]

    events = []
    async for event in provider.chat_completion_stream(model=model, messages=messages):
        events.append(event)

    chat_completion = ToChatCompletion.from_chat_completion_events(events)

    assert len(chat_completion.message.content) == 0
    assert chat_completion.message.name is None
    assert chat_completion.message.role == "assistant"
    assert len(chat_completion.message.tool_calls) == 1
    assert chat_completion.message.tool_calls[0].id == "call_PieqNSej6kM9hgYbcQdbZSaC"
    assert chat_completion.message.tool_calls[0].name == "get_weather"
    assert chat_completion.message.tool_calls[0].arguments == '{"location": "Tokyo"}'
    assert chat_completion.usage is not None
    assert chat_completion.usage.prompt_tokens == 67
    assert chat_completion.usage.completion_tokens == 31
    assert chat_completion.usage.total_tokens == 98
