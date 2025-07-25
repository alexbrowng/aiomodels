import typing

from types_aiobotocore_bedrock_runtime.type_defs import (
    InferenceConfigurationTypeDef,
    MessageUnionTypeDef,
    SystemContentBlockTypeDef,
    ToolConfigurationTypeDef,
)

from aiomodels.messages.message import Message
from aiomodels.messages.system_message import SystemMessage
from aiomodels.parameters.parameters import Parameters
from aiomodels.providers.bedrock.from_message import FromMessage
from aiomodels.providers.bedrock.from_parameters import FromParameters
from aiomodels.providers.bedrock.from_tool import FromTool
from aiomodels.response_formats.response_format import ResponseFormat
from aiomodels.tools.tool import Tool
from aiomodels.tools.tools import Tools


class RequestArgs(typing.TypedDict):
    modelId: str
    system: typing.NotRequired[typing.Sequence[SystemContentBlockTypeDef]]
    messages: typing.NotRequired[typing.Sequence[MessageUnionTypeDef]]
    inferenceConfig: typing.NotRequired[InferenceConfigurationTypeDef]
    toolConfig: typing.NotRequired[ToolConfigurationTypeDef]


class FromArgs:
    @staticmethod
    def from_args(
        model_id: str,
        messages: typing.Sequence[Message],
        tools: Tools | typing.Sequence[Tool] | None = None,
        parameters: Parameters | None = None,
        response_format: ResponseFormat | None = None,
    ) -> RequestArgs:
        request = RequestArgs(
            modelId=model_id,
            system=[
                FromMessage.from_system_message(message) for message in messages if isinstance(message, SystemMessage)
            ],
            messages=[
                FromMessage.from_message(message) for message in messages if not isinstance(message, SystemMessage)
            ],
        )

        if parameters:
            request["inferenceConfig"] = FromParameters.from_parameters(parameters)

        if tools:
            request["toolConfig"] = FromTool.from_tools(tools)

        return request
