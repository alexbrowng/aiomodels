import typing

from openai.types.chat.chat_completion_chunk import ChatCompletionChunk, ChoiceDeltaToolCall
from openai.types.completion_usage import CompletionUsage

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
from aiomodels.providers.openai.primitives import ContentBlock, ToolCallBlock

ContentContentType = typing.Literal["text", "json"]


class ToChatCompletionEvent:
    def __init__(
        self,
        stream: typing.AsyncIterable[ChatCompletionChunk],
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
        self._blocks: list[ContentBlock | ToolCallBlock] = []

    def _has_content_block(self) -> bool:
        return any(block["type"] == "content" for block in self._blocks)

    def _is_last_block_content(self) -> bool:
        return self._has_content_block() and self._blocks[-1]["type"] == "content"

    def _has_tool_call_block(self) -> bool:
        return any(block["type"] == "tool_call" for block in self._blocks)

    def _is_last_block_tool_call(self) -> bool:
        return self._has_tool_call_block() and self._blocks[-1]["type"] == "tool_call"

    def _on_message_start(self) -> MessageStartEvent:
        return ChatCompletionEventFactory.message_start(model=self._model.id, name=self._message_name)

    def _content_start(self, content: str | None = None) -> ContentStartEvent:
        index = sum(1 for block in self._blocks if block["type"] == "content")
        block = ContentBlock(index=index, type="content")
        self._blocks.append(block)
        return ChatCompletionEventFactory.content_start(
            index=index,
            content_type=self._content_type,
            content=content,
            name=self._content_name,
        )

    def _content_delta(self, delta: str) -> ContentDeltaEvent:
        block = self._blocks[-1]

        if block["type"] != "content":
            raise ValueError("Content block not found")

        return ChatCompletionEventFactory.content_delta(index=block["index"], delta=delta)

    def _content_finish(self) -> ContentFinishEvent:
        block = self._blocks[-1]

        if block["type"] != "content":
            raise ValueError("Content block not found")

        return ChatCompletionEventFactory.content_finish(index=block["index"])

    def _on_delta_content(self, content: str) -> ContentStartEvent | ContentDeltaEvent:
        if not self._is_last_block_content():
            return self._content_start(content)
        else:
            return self._content_delta(content)

    def _tool_call_start(self, tool_call: ChoiceDeltaToolCall) -> ToolCallStartEvent:
        id = tool_call.id
        name = tool_call.function.name if tool_call.function else None
        arguments = tool_call.function.arguments if tool_call.function else None

        if not id or not name:
            raise ValueError("Tool call id or name not found")

        block = ToolCallBlock(index=tool_call.index, id=id, type="tool_call")
        self._blocks.append(block)

        return ChatCompletionEventFactory.tool_call_start(id=id, name=name, arguments=arguments)

    def _tool_call_delta(self, arguments: str) -> ToolCallDeltaEvent:
        block = self._blocks[-1]

        if block["type"] != "tool_call":
            raise ValueError("Tool call block not found")

        return ChatCompletionEventFactory.tool_call_delta(id=block["id"], arguments=arguments)

    def _tool_call_finish(self) -> ToolCallFinishEvent:
        block = self._blocks[-1]

        if block["type"] != "tool_call":
            raise ValueError("Tool call block not found")

        return ChatCompletionEventFactory.tool_call_finish(id=block["id"])

    def _on_delta_tool_calls(
        self, tool_calls: list[ChoiceDeltaToolCall]
    ) -> typing.Iterator[ToolCallStartEvent | ToolCallDeltaEvent | ToolCallFinishEvent]:
        for tool_call in tool_calls:
            if not self._is_last_block_tool_call():
                yield self._tool_call_start(tool_call)
            elif self._blocks[-1]["index"] == tool_call.index:
                arguments = tool_call.function.arguments if tool_call.function else None

                if not arguments:
                    return

                yield self._tool_call_delta(arguments)
            else:
                yield self._tool_call_finish()
                yield self._tool_call_start(tool_call)

    def _on_message_finish(self, reason: typing.Literal["stop", "tool_calls", "length"]) -> MessageFinishEvent:
        return ChatCompletionEventFactory.message_finish(reason=reason)

    def _on_message_usage(self, usage: CompletionUsage) -> MessageUsageEvent:
        return ChatCompletionEventFactory.message_usage(
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
        )

    async def __aiter__(self) -> typing.AsyncIterator[ChatCompletionEvent]:
        yield self._on_message_start()

        async for chunk in self._stream:
            if chunk.usage:
                yield self._on_message_usage(chunk.usage)

            if not chunk.choices:
                continue

            if chunk.choices[0].delta.content:
                if self._is_last_block_tool_call():
                    yield self._tool_call_finish()

                yield self._on_delta_content(chunk.choices[0].delta.content)

            if chunk.choices[0].delta.tool_calls:
                if self._is_last_block_content():
                    yield self._content_finish()

                for event in self._on_delta_tool_calls(chunk.choices[0].delta.tool_calls):
                    yield event

            if chunk.choices[0].finish_reason:
                if self._is_last_block_content():
                    yield self._content_finish()

                if self._is_last_block_tool_call():
                    yield self._tool_call_finish()

                if chunk.choices[0].finish_reason == "tool_calls":
                    finish_reason = "tool_calls"
                elif chunk.choices[0].finish_reason == "length":
                    finish_reason = "length"
                else:
                    finish_reason = "stop"

                yield self._on_message_finish(reason=finish_reason)
