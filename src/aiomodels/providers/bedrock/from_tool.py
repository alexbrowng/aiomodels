import typing

from types_aiobotocore_bedrock_runtime.type_defs import ToolConfigurationTypeDef, ToolTypeDef

from aiomodels.tools.tool import Tool
from aiomodels.tools.tools import Tools


class FromTool:
    @staticmethod
    def from_tool(tool: Tool) -> ToolTypeDef:
        return {
            "toolSpec": {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": {"json": tool.parameters.to_primitives()},
            }
        }

    @staticmethod
    def from_tools(tools: Tools | typing.Sequence[Tool]) -> ToolConfigurationTypeDef:
        return {"tools": [FromTool.from_tool(tool) for tool in tools]}
