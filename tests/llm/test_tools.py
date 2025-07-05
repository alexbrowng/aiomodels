from aiomodels.tools.tool import Tool
from aiomodels.tools.tool_call import ToolCall


def test_tool_creation():
    tool = Tool(
        name="get_weather",
        description="Get weather info",
        parameters={"location": {"type": "string"}},
        strict=True,
    )
    assert tool.name == "get_weather"
    assert tool.description == "Get weather info"
    assert tool.parameters == {"location": {"type": "string"}}
    assert tool.strict is True


def test_tool_call_creation():
    call = ToolCall(id="call1", name="get_weather", arguments={"location": "Paris"})
    assert call.id == "call1"
    assert call.name == "get_weather"
    assert call.arguments == {"location": "Paris"}
