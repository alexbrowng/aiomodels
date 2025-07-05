import os

from aiomodels.providers.openai.provider import OpenAIProvider


class GoogleOpenAICompatibleProvider(OpenAIProvider):
    def __init__(
        self,
        base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai",
        api_key: str | None = os.getenv("GOOGLE_API_KEY"),
    ):
        super().__init__(base_url=base_url, api_key=api_key)
