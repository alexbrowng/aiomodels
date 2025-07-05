import asyncio

from aiomodels.messages.system_message import SystemMessage
from aiomodels.messages.user_message import UserMessage
from aiomodels.models.model import Model
from aiomodels.parameters.parameters import Parameters
from aiomodels.providers.bedrock.provider import BedrockProvider
from examples.tools.tools import tools


async def run():
    llm = BedrockProvider()

    messages = [
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="What is the weather in Tokyo?"),
    ]

    model = Model(id="us.anthropic.claude-3-7-sonnet-20250219-v1:0", name="Claude 3.7 Sonnet", provider="Bedrock")

    parameters = Parameters(max_tokens=256, temperature=0.2)

    chat_completion = await llm.chat_completion(
        model=model,
        messages=messages,
        tools=tools,
        parameters=parameters,
        name="assistant",
    )
    print(chat_completion)

    messages.append(chat_completion.message)

    if chat_completion.finish_reason == "tool_calls":
        tool_messages = await tools.calls(chat_completion.message.tool_calls)
        messages.extend(tool_messages)

    chat_completion = await llm.chat_completion(
        model=model,
        messages=messages,
        tools=tools,
        parameters=parameters,
        name="assistant",
    )

    print(chat_completion)


if __name__ == "__main__":
    asyncio.run(run())
