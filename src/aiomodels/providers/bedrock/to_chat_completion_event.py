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
from aiomodels.chat_completion_events.content_start_event import ContentStartEvent
from aiomodels.chat_completion_events.message_finish_event import MessageFinishEvent
from aiomodels.chat_completion_events.message_start_event import MessageStartEvent
from aiomodels.chat_completion_events.message_usage_event import MessageUsageEvent
from aiomodels.chat_completion_events.tool_call_event import ToolCallEvent
from aiomodels.models.model import Model

ContentContentType = typing.Literal["text", "json", "refusal"]


class ToChatCompletionEvent:
    def __init__(
        self,
        response: ConverseStreamResponseTypeDef,
        model: Model,
        content_type: ContentContentType = "text",
        name: str | None = None,
    ):
        self._stream = response["stream"]
        self._model = model
        self._content_type: ContentContentType = content_type
        self._name = name
        self._tool_calls = []

    def _message_start_event(self) -> MessageStartEvent:
        return ChatCompletionEventFactory.message_start(model=self._model.id, name=self._name)

    def _content_start_event(self, index: int, content_type: ContentContentType) -> ContentStartEvent:
        return ChatCompletionEventFactory.content_start(index=index, content_type=content_type)

    def _content_delta_event(self, index: int, delta: str) -> ContentDeltaEvent:
        return ChatCompletionEventFactory.content_delta(index=index, delta=delta)

    def _message_finish_event(self, finish_reason: typing.Literal["stop", "tool_calls"]) -> MessageFinishEvent:
        return ChatCompletionEventFactory.message_finish(reason=finish_reason)

    def _start_tool_call(self, tool_use: ToolUseBlockStartTypeDef):
        self._tool_calls.append(
            {
                "id": tool_use["toolUseId"],
                "name": tool_use["name"],
                "arguments": tool_use.get("input", ""),
            }
        )

    def _merge_tool_calls(self, tool_use: ToolUseBlockDeltaTypeDef):
        tool_call = self._tool_calls[-1]
        tool_call["arguments"] += tool_use.get("input", "")

    def _tool_call_events(self) -> typing.Sequence[ToolCallEvent]:
        return [
            ChatCompletionEventFactory.tool_call(
                id=tool_call.get("id", ""),
                name=tool_call.get("name", ""),
                arguments=tool_call.get("arguments"),
            )
            for tool_call in self._tool_calls
        ]

    def _message_usage_event(self, usage: TokenUsageTypeDef) -> MessageUsageEvent:
        return ChatCompletionEventFactory.message_usage(
            prompt_tokens=usage["inputTokens"],
            completion_tokens=usage["outputTokens"],
            total_tokens=usage["totalTokens"],
        )

    async def __aiter__(self) -> typing.AsyncIterator[ChatCompletionEvent]:
        index = -1

        async for chunk in self._stream:
            if "messageStart" in chunk:
                yield self._message_start_event()

            if "contentBlockStart" in chunk:
                if "toolUse" in chunk["contentBlockStart"]["start"]:
                    self._start_tool_call(chunk["contentBlockStart"]["start"]["toolUse"])

                if "text" in chunk["contentBlockStart"]["start"]:
                    index += 1
                    yield self._content_start_event(index=index, content_type=self._content_type)

            if "contentBlockDelta" in chunk and chunk["contentBlockDelta"]["delta"]:
                if "text" in chunk["contentBlockDelta"]["delta"]:
                    yield self._content_delta_event(
                        index=index,
                        delta=chunk["contentBlockDelta"]["delta"]["text"],
                    )

                if "toolUse" in chunk["contentBlockDelta"]["delta"]:
                    self._merge_tool_calls(chunk["contentBlockDelta"]["delta"]["toolUse"])

            if "messageStop" in chunk:
                if chunk["messageStop"]["stopReason"] == "stop":
                    yield self._message_finish_event(finish_reason="stop")

                if chunk["messageStop"]["stopReason"] == "tool_use":
                    for tool_call_event in self._tool_call_events():
                        yield tool_call_event

                    yield self._message_finish_event(finish_reason="tool_calls")

            if usage := chunk.get("metadata", {}).get("usage"):
                yield self._message_usage_event(usage)
