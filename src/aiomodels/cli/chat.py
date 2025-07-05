import argparse
import asyncio
import typing

from aiomodels.chat_completion_events.chat_completion_event import ChatCompletionEvent
from aiomodels.chat_completion_events.to_chat_completion import ToChatCompletion
from aiomodels.messages.message import Message
from aiomodels.messages.system_message import SystemMessage
from aiomodels.messages.user_message import UserMessage
from aiomodels.models.model import Model, ModelPrice
from aiomodels.parameters.parameters import Parameters
from aiomodels.providers.helpers.loader import load_provider_from_model


async def chat(model: Model, parameters: Parameters, instructions: str | None, name: str | None = None):
    provider = load_provider_from_model(model)

    messages: typing.Sequence[Message] = []

    if instructions:
        messages.append(SystemMessage(content=instructions))

    while True:
        prompt = input("User: ")

        user_message = UserMessage(content=prompt)
        messages.append(user_message)

        events: typing.Sequence[ChatCompletionEvent] = []

        print("Assistant: ", end="", flush=True)
        async for event in provider.chat_completion_stream(
            model=model,
            messages=messages,
            parameters=parameters,
            name=name,
        ):
            events.append(event)

            if event.type == "content_delta":
                print(event.delta, end="", flush=True)

            if event.type == "finish" and event.finish_reason == "stop":
                print()

        chat_completion = ToChatCompletion.from_chat_completion_events(events)
        messages.append(chat_completion.message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="openai:gpt-4o-mini")
    parser.add_argument("--model-name", type=str, default=None)
    parser.add_argument("--instructions", type=str, default=None)
    parser.add_argument("--input-price", type=float, default=None)
    parser.add_argument("--output-price", type=float, default=None)
    parser.add_argument("--temperature", type=float, default=None)
    parser.add_argument("--top-p", type=float, default=None)
    parser.add_argument("--max-tokens", type=int, default=None)
    parser.add_argument("--frequency-penalty", type=float, default=None)
    parser.add_argument("--presence-penalty", type=float, default=None)
    parser.add_argument("--stop", type=str, default=None)
    parser.add_argument("--name", type=str, default=None)

    args = parser.parse_args()

    if not args.model or ":" not in args.model:
        parser.error("Argument --model must be in the format 'provider:model_id'")

    provider_name, model_id = args.model.split(":", 1)

    model = Model(
        model_id,
        name=args.model_name or model_id,
        provider=provider_name,
        price=ModelPrice(
            input=args.input_price,
            output=args.output_price,
        ),
    )

    parameters = Parameters(
        temperature=args.temperature,
        top_p=args.top_p,
        max_tokens=args.max_tokens,
        frequency_penalty=args.frequency_penalty,
        presence_penalty=args.presence_penalty,
        stop=args.stop,
    )

    asyncio.run(chat(model=model, parameters=parameters, instructions=args.instructions, name=args.name))
