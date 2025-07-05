from aiomodels.chat_completions.chat_completion import ChatCompletion
from aiomodels.contents.text_content import TextContent
from aiomodels.providers.bedrock.to_chat_completion import ToChatCompletion
from aiomodels.tools.tool_call import ToolCall


def make_converse_response_text():
    return {
        "output": {"message": {"content": [{"text": "Hello world!"}]}},
        "usage": {"inputTokens": 10, "outputTokens": 5, "totalTokens": 15},
        "stopReason": "stop",
    }


def make_converse_response_tool_call():
    return {
        "output": {
            "message": {
                "content": [{"toolUse": {"toolUseId": "call1", "name": "get_weather", "input": {"location": "Paris"}}}]
            }
        },
        "usage": {"inputTokens": 2, "outputTokens": 3, "totalTokens": 5},
        "stopReason": "tool_use",
    }


def make_converse_response_text_and_tool():
    return {
        "output": {
            "message": {
                "content": [{"text": "Hi!"}, {"toolUse": {"toolUseId": "call2", "name": "get_time", "input": {}}}]
            }
        },
        "usage": {"inputTokens": 7, "outputTokens": 8, "totalTokens": 15},
        "stopReason": "tool_use",
    }


def test_to_chat_completion_text_only():
    response = make_converse_response_text()
    chat = ToChatCompletion.from_converse_response(response)  # type: ignore
    assert isinstance(chat, ChatCompletion)
    assert len(chat.message.content) == 1
    assert isinstance(chat.message.content[0], TextContent)
    assert chat.message.content[0].text == "Hello world!"
    assert chat.message.tool_calls == []
    assert chat.finish_reason == "stop"
    assert chat.usage is not None
    assert chat.usage.prompt_tokens == 10
    assert chat.usage.completion_tokens == 5
    assert chat.usage.total_tokens == 15


def test_to_chat_completion_tool_call():
    response = make_converse_response_tool_call()
    chat = ToChatCompletion.from_converse_response(response)  # type: ignore
    assert chat.finish_reason == "tool_calls"
    assert len(chat.message.tool_calls) == 1
    tool_call = chat.message.tool_calls[0]
    assert isinstance(tool_call, ToolCall)
    assert tool_call.id == "call1"
    assert tool_call.name == "get_weather"
    assert tool_call.arguments == {"location": "Paris"}
    assert chat.message.content == []
    assert chat.usage is not None
    assert chat.usage.total_tokens == 5


def test_to_chat_completion_text_and_tool():
    response = make_converse_response_text_and_tool()
    chat = ToChatCompletion.from_converse_response(response, name="asst1")  # type: ignore
    assert chat.message.name == "asst1"
    assert len(chat.message.content) == 1
    assert isinstance(chat.message.content[0], TextContent)
    assert chat.message.content[0].text == "Hi!"
    assert len(chat.message.tool_calls) == 1
    assert chat.message.tool_calls[0].id == "call2"
    assert chat.message.tool_calls[0].name == "get_time"
    assert chat.message.tool_calls[0].arguments == {}
    assert chat.finish_reason == "tool_calls"
    assert chat.usage is not None
    assert chat.usage.prompt_tokens == 7
    assert chat.usage.completion_tokens == 8
    assert chat.usage.total_tokens == 15
