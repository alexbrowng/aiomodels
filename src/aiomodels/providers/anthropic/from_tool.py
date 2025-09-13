import typing

from anthropic.types.tool_param import ToolParam

from aiomodels.tools.tool import Tool
from aiomodels.tools.tools import Tools


class FromTool:
    @staticmethod
    def from_tool(tool: Tool) -> ToolParam:
        return {
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.parameters.to_primitives(),
        }

    @staticmethod
    def from_tools(tools: Tools | typing.Sequence[Tool]) -> list[ToolParam]:
        return [FromTool.from_tool(tool) for tool in tools]
