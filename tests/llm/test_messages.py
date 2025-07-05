import json
import typing

from aiomodels.contents.image_content import ImageContent
from aiomodels.contents.text_content import TextContent
from aiomodels.messages.assistant_message import AssistantMessage
from aiomodels.messages.system_message import SystemMessage
from aiomodels.messages.tool_message import ToolMessage
from aiomodels.messages.user_message import UserMessage
from aiomodels.sources.base64_source import Base64Source
from aiomodels.tools.tool_call import ToolCall
from aiomodels.tools.tool_result import ToolResult


def test_system_message_creation():
    msg = SystemMessage(content="Test system")
    assert msg.content == "Test system"
    assert msg.role == "system"


def test_user_message_with_text_content():
    content: typing.Sequence[TextContent | ImageContent] = [TextContent(text="Hello!")]
    msg = UserMessage(content=content, name="user1")
    assert msg.content == content
    assert msg.name == "user1"
    assert msg.role == "user"


def test_user_message_with_image_content():
    img = ImageContent(source=Base64Source(data="abc", media_type="image/png"), detail="high")
    content: typing.Sequence[TextContent | ImageContent] = [img]
    msg = UserMessage(content=content)
    assert isinstance(msg.content[0], ImageContent)
    assert msg.content[0].source.url == "data:image/png;base64,abc"
    assert msg.content[0].detail == "high"
    assert msg.role == "user"


def test_assistant_message_with_tool_calls():
    content = [TextContent(text="Hi!")]
    tool_calls = [ToolCall(id="call1", name="tool", arguments=json.dumps({"foo": "bar"}))]
    msg = AssistantMessage(content=content, tool_calls=tool_calls, name="asst1")
    assert msg.content == content
    assert msg.tool_calls == tool_calls
    assert msg.name == "asst1"
    assert msg.role == "assistant"


def test_tool_message_creation():
    msg = ToolMessage(tool_result=ToolResult(id="call1", name="tool", result='{"foo": "bar"}'))
    assert msg.tool_result == ToolResult(id="call1", name="tool", result='{"foo": "bar"}')
    assert msg.role == "tool"
