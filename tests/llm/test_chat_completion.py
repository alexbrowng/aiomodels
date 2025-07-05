from aiomodels.chat_completions.chat_completion import ChatCompletion
from aiomodels.contents.text_content import TextContent
from aiomodels.messages.assistant_message import AssistantMessage
from aiomodels.usage.usage import Usage


def test_chat_completion_creation():
    message = AssistantMessage(content=[TextContent(text="Hi!")], tool_calls=[])
    usage = Usage(prompt_tokens=10, completion_tokens=5, total_tokens=15)
    chat = ChatCompletion(finish_reason="stop", message=message, usage=usage)
    assert chat.message == message
    assert chat.usage == usage
    assert chat.finish_reason == "stop"
