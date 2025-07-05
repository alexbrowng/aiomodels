import typing

from aiomodels.contents.image_content import ImageContent
from aiomodels.contents.text_content import TextContent
from aiomodels.json_schema.object import Object
from aiomodels.json_schema.property import Property
from aiomodels.json_schema.string import String
from aiomodels.messages.system_message import SystemMessage
from aiomodels.messages.user_message import UserMessage
from aiomodels.models.model import Model, ModelPrice
from aiomodels.parameters.parameters import Parameters
from aiomodels.sources.base64_source import Base64Source
from aiomodels.tools.tool import Tool


def make_model(
    id: str = "gpt-4o-mini",
    name: str = "GPT 4o mini",
    provider: str = "OpenAI",
    input_price: float | None = None,
    output_price: float | None = None,
) -> Model:
    return Model(id=id, name=name, provider=provider, price=ModelPrice(input=input_price, output=output_price))


def make_text_content(text: str = "Hello!") -> TextContent:
    return TextContent(text=text)


def make_image_content(
    data: str = "abc",
    media_type: str = "image/png",
    detail: typing.Literal["auto", "low", "high"] = "auto",
) -> ImageContent:
    return ImageContent(source=Base64Source(data=data, media_type=media_type), detail=detail)


def make_user_message(
    content: typing.Sequence[TextContent | ImageContent] | None = None,
    name: str | None = None,
) -> UserMessage:
    if content is None:
        content = [make_text_content()]
    return UserMessage(content=content, name=name)


def make_system_message(
    content: str = "You are a helpful assistant.",
) -> SystemMessage:
    return SystemMessage(content=content)


def make_tool(
    name: str = "get_weather",
    description: str = "Get the weather for a location.",
    parameters: Object | None = None,
    strict: bool = False,
) -> Tool:
    if parameters is None:
        parameters = Object(Property("location", String("Location to get weather for.")))
    return Tool(name=name, description=description, parameters=parameters, strict=strict)


def make_parameters(
    max_tokens: int | None = 16,
    temperature: float | None = 0.7,
    top_p: float | None = 1.0,
    frequency_penalty: float | None = 0.0,
    presence_penalty: float | None = 0.0,
    stop: list[str] | None = None,
) -> Parameters:
    return Parameters(
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop,
    )
