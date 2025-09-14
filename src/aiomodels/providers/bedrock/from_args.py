import typing

from types_aiobotocore_bedrock_runtime.type_defs import (
    InferenceConfigurationTypeDef,
    MessageUnionTypeDef,
    SystemContentBlockTypeDef,
    ToolConfigurationTypeDef,
)

from aiomodels.messages.message import Message
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
        messages_param, system_param = FromMessage.from_messages(messages)

        request = RequestArgs(modelId=model_id, messages=messages_param)

        if tools:
            system_param.extend(FromMessage.from_tools(tools))
            request["toolConfig"] = FromTool.from_tools(tools)

        if system_param:
            request["system"] = system_param

        if parameters:
            request["inferenceConfig"] = FromParameters.from_parameters(parameters)

        return request
