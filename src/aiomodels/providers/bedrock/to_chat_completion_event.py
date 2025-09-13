import typing

from types_aiobotocore_bedrock_runtime.type_defs import (
    ConverseStreamResponseTypeDef,
    TokenUsageTypeDef,
    ToolUseBlockDeltaTypeDef,
    ToolUseBlockStartTypeDef,
)

from aiomodels.chat_completion_events.chat_completion_event import ChatCompletionEvent
from aiomodels.chat_completion_events.chat_completion_event_factory import ChatCompletionEventFactory
from aiomodels.chat_completion_events.content_delta_event import ContentDeltaEvent
from aiomodels.chat_completion_events.content_finish_event import ContentFinishEvent
from aiomodels.chat_completion_events.content_start_event import ContentStartEvent
from aiomodels.chat_completion_events.message_finish_event import MessageFinishEvent
from aiomodels.chat_completion_events.message_start_event import MessageStartEvent
from aiomodels.chat_completion_events.message_usage_event import MessageUsageEvent
from aiomodels.chat_completion_events.tool_call_delta_event import ToolCallDeltaEvent
from aiomodels.chat_completion_events.tool_call_finish_event import ToolCallFinishEvent
from aiomodels.chat_completion_events.tool_call_start_event import ToolCallStartEvent
from aiomodels.models.model import Model
from aiomodels.providers.bedrock.primitives import ContentBlock, ToolUseBlock

ContentContentType = typing.Literal["text", "json"]


class ToChatCompletionEvent:
    def __init__(
        self,
        response: ConverseStreamResponseTypeDef,
        model: Model,
        content_type: ContentContentType = "text",
        content_name: str | None = None,
        message_name: str | None = None,
    ):
        self._stream = response["stream"]
        self._model = model
        self._content_type: ContentContentType = content_type
        self._content_name = content_name
        self._message_name = message_name
        self._blocks: list[ContentBlock | ToolUseBlock] = []

    def _on_message_start(self) -> MessageStartEvent:
        return ChatCompletionEventFactory.message_start(model=self._model.id, name=self._message_name)

    def _on_text_content_block_start(self, content: str | None = None) -> ContentStartEvent:
        index = sum(1 for block in self._blocks if block["type"] == "content")
        block = ContentBlock(index=index, type="content")
        self._blocks.append(block)

        return ChatCompletionEventFactory.content_start(
            index=index,
            content_type=self._content_type,
            content=content,
            name=self._content_name,
        )

    def _on_tool_use_block_start(self, tool_use: ToolUseBlockStartTypeDef) -> ToolCallStartEvent:
        block = ToolUseBlock(id=tool_use["toolUseId"], type="tool_use")
        self._blocks.append(block)
        return ChatCompletionEventFactory.tool_call_start(
            id=tool_use["toolUseId"], name=tool_use["name"], arguments=tool_use.get("input")
        )

    def _on_text_content_block_delta(self, delta: str) -> ContentDeltaEvent:
        block = self._blocks[-1]

        if not block or block["type"] != "content":
            raise ValueError("Content block not found")

        return ChatCompletionEventFactory.content_delta(index=block["index"], delta=delta)

    def _on_tool_use_block_delta(self, tool_use: ToolUseBlockDeltaTypeDef) -> ToolCallDeltaEvent:
        block = self._blocks[-1]

        if not block or block["type"] != "tool_use":
            raise ValueError("Tool use block not found")

        return ChatCompletionEventFactory.tool_call_delta(id=block["id"], arguments=tool_use.get("input"))

    def _on_content_block_stop(self) -> ContentFinishEvent | ToolCallFinishEvent:
        block = self._blocks[-1]

        if not block:
            raise ValueError("Content block not found")
        elif block["type"] == "content":
            return ChatCompletionEventFactory.content_finish(index=block["index"])
        elif block["type"] == "tool_use":
            return ChatCompletionEventFactory.tool_call_finish(id=block["id"])
        else:
            raise ValueError("Content block type not supported")

    def _on_message_stop(self, finish_reason: typing.Literal["stop", "tool_calls", "length"]) -> MessageFinishEvent:
        return ChatCompletionEventFactory.message_finish(reason=finish_reason)

    def _on_message_usage(self, usage: TokenUsageTypeDef) -> MessageUsageEvent:
        return ChatCompletionEventFactory.message_usage(
            prompt_tokens=usage["inputTokens"],
            completion_tokens=usage["outputTokens"],
            total_tokens=usage["totalTokens"],
        )

    async def __aiter__(self) -> typing.AsyncIterator[ChatCompletionEvent]:
        async for chunk in self._stream:
            if "messageStart" in chunk:
                yield self._on_message_start()

            if "contentBlockStart" in chunk:
                if "text" in chunk["contentBlockStart"]["start"]:
                    yield self._on_text_content_block_start()

                if "toolUse" in chunk["contentBlockStart"]["start"]:
                    yield self._on_tool_use_block_start(chunk["contentBlockStart"]["start"]["toolUse"])

            if "contentBlockDelta" in chunk and chunk["contentBlockDelta"]["delta"]:
                if "text" in chunk["contentBlockDelta"]["delta"]:
                    yield self._on_text_content_block_delta(chunk["contentBlockDelta"]["delta"]["text"])

                if "toolUse" in chunk["contentBlockDelta"]["delta"]:
                    yield self._on_tool_use_block_delta(chunk["contentBlockDelta"]["delta"]["toolUse"])

            if "contentBlockStop" in chunk:
                yield self._on_content_block_stop()

            if "messageStop" in chunk:
                finish_reason = "stop"
                if chunk["messageStop"]["stopReason"] == "tool_use":
                    finish_reason = "tool_calls"
                elif chunk["messageStop"]["stopReason"] == "max_tokens":
                    finish_reason = "length"

                yield self._on_message_stop(finish_reason)

            if usage := chunk.get("metadata", {}).get("usage"):
                yield self._on_message_usage(usage)
