import typing

from anthropic import AsyncStream
from anthropic.types import MessageStreamEvent

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
from aiomodels.providers.anthropic.primitives import ContentBlock, ToolUseBlock

ContentContentType = typing.Literal["text", "json"]


class ToChatCompletionEvent:
    def __init__(
        self,
        stream: AsyncStream[MessageStreamEvent],
        model: Model,
        content_type: ContentContentType = "text",
        content_name: str | None = None,
        message_name: str | None = None,
    ):
        self._stream = stream
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

    def _on_tool_use_content_block_start(
        self, tool_use_id: str, name: str, arguments: str | None = None
    ) -> ToolCallStartEvent:
        block = ToolUseBlock(id=tool_use_id, type="tool_use")
        self._blocks.append(block)
        return ChatCompletionEventFactory.tool_call_start(id=tool_use_id, name=name, arguments=arguments)

    def _on_text_content_block_delta(self, delta: str) -> ContentDeltaEvent:
        block = self._blocks[-1]

        if not block or block["type"] != "content":
            raise ValueError("Content block not found")

        return ChatCompletionEventFactory.content_delta(index=block["index"], delta=delta)

    def _on_tool_use_content_block_delta(self, delta: str) -> ToolCallDeltaEvent:
        block = self._blocks[-1]

        if not block or block["type"] != "tool_use":
            raise ValueError("Tool use block not found")

        return ChatCompletionEventFactory.tool_call_delta(id=block["id"], arguments=delta)

    def _on_content_block_finish(self) -> ContentFinishEvent | ToolCallFinishEvent:
        block = self._blocks[-1]

        if not block:
            raise ValueError("Content block not found")
        elif block["type"] == "content":
            return ChatCompletionEventFactory.content_finish(index=block["index"])
        elif block["type"] == "tool_use":
            return ChatCompletionEventFactory.tool_call_finish(id=block["id"])
        else:
            raise ValueError("Content block type not supported")

    def _on_message_finish(self, finish_reason: typing.Literal["stop", "tool_calls", "length"]) -> MessageFinishEvent:
        return ChatCompletionEventFactory.message_finish(reason=finish_reason)

    def _on_message_usage(self, input_tokens: int, output_tokens: int) -> MessageUsageEvent:
        return ChatCompletionEventFactory.message_usage(
            prompt_tokens=input_tokens,
            completion_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
        )

    async def __aiter__(self) -> typing.AsyncIterator[ChatCompletionEvent]:
        input_tokens = 0
        output_tokens = 0
        stop_reason = None

        async for event in self._stream:
            if event.type == "message_start":
                yield self._on_message_start()
                input_tokens += event.message.usage.input_tokens
                output_tokens += event.message.usage.output_tokens

            elif event.type == "content_block_start":
                if event.content_block.type == "text":
                    yield self._on_text_content_block_start(content=event.content_block.text)

                if event.content_block.type == "tool_use":
                    yield self._on_tool_use_content_block_start(event.content_block.id, event.content_block.name)

            elif event.type == "content_block_delta":
                if event.delta.type == "text_delta":
                    yield self._on_text_content_block_delta(event.delta.text)
                elif event.delta.type == "input_json_delta":
                    yield self._on_tool_use_content_block_delta(event.delta.partial_json)

            elif event.type == "content_block_stop":
                yield self._on_content_block_finish()

            elif event.type == "message_delta":
                input_tokens += event.usage.input_tokens or 0
                output_tokens += event.usage.output_tokens
                stop_reason = event.delta.stop_reason

            elif event.type == "message_stop":
                finish_reason = "stop"
                if stop_reason == "max_tokens":
                    finish_reason = "length"
                elif stop_reason == "tool_use" or any(block["type"] == "tool_use" for block in self._blocks):
                    finish_reason = "tool_calls"

                yield self._on_message_finish(finish_reason=finish_reason)
                yield self._on_message_usage(input_tokens=input_tokens, output_tokens=output_tokens)
