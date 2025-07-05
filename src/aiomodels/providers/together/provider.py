import os

from aiomodels.providers.openai.provider import OpenAIProvider


class TogetherProvider(OpenAIProvider):
    def __init__(
        self,
        base_url: str = "https://api.together.xyz/v1",
        api_key: str | None = os.getenv("TOGETHER_API_KEY"),
    ):
        super().__init__(base_url=base_url, api_key=api_key)
