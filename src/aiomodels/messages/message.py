import typing

from aiomodels.messages.assistant_message import AssistantMessage
from aiomodels.messages.system_message import SystemMessage
from aiomodels.messages.tool_message import ToolMessage
from aiomodels.messages.user_message import UserMessage

Message = typing.Union[UserMessage, AssistantMessage, ToolMessage, SystemMessage]
