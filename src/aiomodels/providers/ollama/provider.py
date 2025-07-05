import os

from aiomodels.providers.openai.provider import OpenAIProvider


class OllamaProvider(OpenAIProvider):
    def __init__(
        self,
        base_url: str = "http://localhost:11434/v1",
        api_key: str | None = os.getenv("OLLAMA_API_KEY") or "ollama",
    ):
        super().__init__(base_url=base_url, api_key=api_key)
