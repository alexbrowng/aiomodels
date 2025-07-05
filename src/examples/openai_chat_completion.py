import asyncio

from aiomodels.messages.system_message import SystemMessage
from aiomodels.messages.user_message import UserMessage
from aiomodels.models.model import Model
from aiomodels.parameters.parameters import Parameters
from aiomodels.providers.openai.provider import OpenAIProvider
from aiomodels.response_formats.text_response_format import TextResponseFormat
from examples.tools.tools import tools


async def run():
    llm = OpenAIProvider()

    messages = [
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="What is the weather in Tokyo?"),
    ]

    model = Model(id="gpt-4.1-nano-2025-04-14", name="GPT 4.1 nano", provider="OpenAI")
    parameters = Parameters(max_tokens=256, temperature=0.2)
    response_format = TextResponseFormat()

    chat_completion = await llm.chat_completion(
        model=model,
        messages=messages,
        tools=tools,
        response_format=response_format,
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
        response_format=response_format,
        parameters=parameters,
        name="assistant",
    )
    print(chat_completion)


if __name__ == "__main__":
    asyncio.run(run())
