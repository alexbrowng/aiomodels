import os

from aiomodels.providers.openai.provider import OpenAIProvider


class DeepSeekProvider(OpenAIProvider):
    def __init__(
        self,
        base_url: str = "https://api.deepseek.com/v1",
        api_key: str | None = os.getenv("DEEPSEEK_API_KEY"),
    ):
        super().__init__(base_url=base_url, api_key=api_key)
