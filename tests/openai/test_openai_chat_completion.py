import openai_responses
import pytest

from aiomodels.contents.text_content import TextContent
from aiomodels.messages.system_message import SystemMessage
from aiomodels.messages.user_message import UserMessage
from aiomodels.models.model import Model
from aiomodels.providers.openai.provider import OpenAIProvider
from tests.openai.object_mothers import (
    make_image_content,
    make_model,
    make_parameters,
    make_system_message,
    make_tool,
    make_user_message,
)


@pytest.mark.asyncio
@openai_responses.mock()
async def test_async_create_chat_completion(openai_mock: openai_responses.OpenAIMock):
    openai_mock.chat.completions.create.response = {
        "choices": [
            {
                "index": 0,
                "finish_reason": "stop",
                "message": {"content": "Hello! How can I help?", "role": "assistant"},
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20},
    }

    provider = OpenAIProvider(api_key="sk-fake123")
    model = Model(id="gpt-4o-mini", name="GPT 4o mini", provider="OpenAI")
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content=[TextContent(text="Hello!")]),
    ]
    chat_completion = await provider.chat_completion(model=model, messages=messages)

    assert len(chat_completion.message.content) == 1
    assert isinstance(chat_completion.message.content[0], TextContent)
    assert chat_completion.message.content[0].text == "Hello! How can I help?"
    assert chat_completion.message.name is None
    assert chat_completion.message.role == "assistant"
    assert chat_completion.message.tool_calls == []
    assert chat_completion.usage is not None
    assert chat_completion.usage.prompt_tokens == 10
    assert chat_completion.usage.completion_tokens == 10
    assert chat_completion.usage.total_tokens == 20
    assert openai_mock.chat.completions.create.route.call_count == 1


@pytest.mark.asyncio
@openai_responses.mock()
async def test_async_create_chat_completion_with_tool(openai_mock):
    openai_mock.chat.completions.create.response = {
        "choices": [
            {
                "index": 0,
                "finish_reason": "stop",
                "message": {
                    "content": None,
                    "role": "assistant",
                    "tool_calls": [
                        {
                            "id": "call_123",
                            "type": "function",
                            "function": {"name": "get_weather", "arguments": '{"location": "Tokyo"}'},
                        }
                    ],
                },
            }
        ],
        "usage": {"prompt_tokens": 15, "completion_tokens": 5, "total_tokens": 20},
    }
    provider = OpenAIProvider(api_key="sk-fake123")
    model = make_model()
    messages = [make_system_message(), make_user_message()]
    tools = [make_tool()]
    chat_completion = await provider.chat_completion(model=model, messages=messages, tools=tools)
    assert chat_completion.message.tool_calls[0].name == "get_weather"
    assert chat_completion.message.tool_calls[0].arguments == '{"location": "Tokyo"}'
    assert chat_completion.usage is not None
    assert chat_completion.usage.prompt_tokens == 15
    assert chat_completion.usage.completion_tokens == 5
    assert chat_completion.usage.total_tokens == 20


@pytest.mark.asyncio
@openai_responses.mock()
async def test_async_create_chat_completion_with_parameters(openai_mock):
    openai_mock.chat.completions.create.response = {
        "choices": [
            {
                "index": 0,
                "finish_reason": "stop",
                "message": {"content": "Hola mundo!", "role": "assistant"},
            }
        ],
        "usage": {"prompt_tokens": 5, "completion_tokens": 2, "total_tokens": 7},
    }
    provider = OpenAIProvider(api_key="sk-fake123")
    model = make_model()
    messages = [make_system_message(), make_user_message()]
    parameters = make_parameters(max_tokens=5, temperature=0.1)
    chat_completion = await provider.chat_completion(model=model, messages=messages, parameters=parameters)
    assert len(chat_completion.message.content) == 1
    assert isinstance(chat_completion.message.content[0], TextContent)
    assert chat_completion.message.content[0].text == "Hola mundo!"
    assert chat_completion.usage is not None
    assert chat_completion.usage.prompt_tokens == 5
    assert chat_completion.usage.completion_tokens == 2
    assert chat_completion.usage.total_tokens == 7


@pytest.mark.asyncio
@openai_responses.mock()
async def test_async_create_chat_completion_with_image_content(openai_mock):
    openai_mock.chat.completions.create.response = {
        "choices": [
            {
                "index": 0,
                "finish_reason": "stop",
                "message": {"content": "Nice image!", "role": "assistant"},
            }
        ],
        "usage": {"prompt_tokens": 8, "completion_tokens": 3, "total_tokens": 11},
    }
    provider = OpenAIProvider(api_key="sk-fake123")
    model = make_model()
    image_content = make_image_content()
    messages = [make_system_message(), make_user_message(content=[image_content])]
    chat_completion = await provider.chat_completion(model=model, messages=messages)
    assert len(chat_completion.message.content) == 1
    assert isinstance(chat_completion.message.content[0], TextContent)
    assert chat_completion.message.content[0].text == "Nice image!"
    assert chat_completion.usage is not None
    assert chat_completion.usage.prompt_tokens == 8
    assert chat_completion.usage.completion_tokens == 3
    assert chat_completion.usage.total_tokens == 11
