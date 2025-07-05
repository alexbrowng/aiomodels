import os

from aiomodels.providers.openai.provider import OpenAIProvider


class OpenRouterProvider(OpenAIProvider):
    def __init__(
        self,
        base_url: str = "https://openrouter.ai/api/v1",
        api_key: str | None = os.getenv("OPENROUTER_API_KEY"),
    ):
        super().__init__(base_url=base_url, api_key=api_key)
