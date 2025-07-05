from unittest.mock import AsyncMock, patch

import pytest
import respx
from aiomodels.chat_completions.chat_completion import ChatCompletion
from aiomodels.contents.text_content import TextContent
from aiomodels.messages.system_message import SystemMessage
from aiomodels.messages.user_message import UserMessage
from aiomodels.models.model import Model
from aiomodels.providers.bedrock.provider import BedrockProvider


@pytest.mark.asyncio
@respx.mock
async def test_bedrock_llm_chat_completion():
    model = Model(id="anthropic.claude-v2", name="Claude v2", provider="Bedrock")
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content=[TextContent(text="Hello!")]),
    ]

    fake_response = {
        "output": {"message": {"content": [{"text": "Hello from Bedrock!"}]}},
        "usage": {"inputTokens": 10, "outputTokens": 5, "totalTokens": 15},
        "stopReason": "stop",
    }

    with patch("aioboto3.Session.client") as mock_client:
        mock_client_instance = mock_client.return_value.__aenter__.return_value
        mock_client_instance.converse = AsyncMock(return_value=fake_response)

        provider = BedrockProvider()
        chat_completion = await provider.chat_completion(model=model, messages=messages)

        assert isinstance(chat_completion, ChatCompletion)
        assert len(chat_completion.message.content) == 1
        assert isinstance(chat_completion.message.content[0], TextContent)
        assert chat_completion.message.content[0].text == "Hello from Bedrock!"
        assert chat_completion.usage is not None
        assert chat_completion.usage.prompt_tokens == 10
        assert chat_completion.usage.completion_tokens == 5
        assert chat_completion.usage.total_tokens == 15
        assert chat_completion.finish_reason == "stop"
