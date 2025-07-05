import asyncio
import pathlib

from aiomodels.contents.audio_content import AudioContent
from aiomodels.contents.text_content import TextContent
from aiomodels.messages.system_message import SystemMessage
from aiomodels.messages.user_message import UserMessage
from aiomodels.models.model import Model
from aiomodels.parameters.parameters import Parameters
from aiomodels.providers.openai.provider import OpenAIProvider
from aiomodels.response_formats.text_response_format import TextResponseFormat
from aiomodels.sources.base64_source import Base64Source

BASE_PATH = pathlib.Path(__file__).parent
DATA_PATH = BASE_PATH / "data"
AUDIO_PATH = DATA_PATH / "audios"


async def run():
    llm = OpenAIProvider()

    audio_path = AUDIO_PATH / "hola.mp3"
    audio = Base64Source.from_file_path(audio_path)

    messages = [
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content=[TextContent(text="What is the content of the audio?"), AudioContent(source=audio)]),
    ]

    model = Model(id="gpt-4o-audio-preview-2024-10-01", name="GPT 4o mini", provider="OpenAI")
    parameters = Parameters(max_tokens=256, temperature=0.2)
    response_format = TextResponseFormat()
    chat_completion = await llm.chat_completion(
        model=model,
        messages=messages,
        parameters=parameters,
        response_format=response_format,
        name="assistant",
    )
    print(chat_completion)


if __name__ == "__main__":
    asyncio.run(run())
