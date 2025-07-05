import os

from aiomodels.providers.openai.provider import OpenAIProvider


class PerplexityProvider(OpenAIProvider):
    def __init__(
        self,
        base_url: str = "https://api.perplexity.ai",
        api_key: str | None = os.getenv("PERPLEXITY_API_KEY"),
    ):
        super().__init__(base_url=base_url, api_key=api_key)
