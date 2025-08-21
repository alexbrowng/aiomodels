from aiomodels.models.model import Model
from aiomodels.providers import (
    AIMLProvider,
    AnthropicOpenAICompatibleProvider,
    AnthropicProvider,
    BedrockProvider,
    ChutesProvider,
    DeepSeekProvider,
    FireworksProvider,
    GoogleOpenAICompatibleProvider,
    GroqProvider,
    InceptionProvider,
    MinimaxProvider,
    MistralProvider,
    OllamaProvider,
    OpenAIProvider,
    OpenRouterProvider,
    PerplexityProvider,
    RekaProvider,
    TogetherProvider,
    XAIProvider,
)
from aiomodels.providers.provider import Provider

LLM_PROVIDERS = {
    "aiml": AIMLProvider,
    "anthropic": AnthropicProvider,
    "anthropic_openai_compatible": AnthropicOpenAICompatibleProvider,
    "bedrock": BedrockProvider,
    "chutes": ChutesProvider,
    "deepseek": DeepSeekProvider,
    "fireworks": FireworksProvider,
    "google_openai_compatible": GoogleOpenAICompatibleProvider,
    "groq": GroqProvider,
    "inception": InceptionProvider,
    "minimax": MinimaxProvider,
    "mistral": MistralProvider,
    "ollama": OllamaProvider,
    "openai": OpenAIProvider,
    "openrouter": OpenRouterProvider,
    "perplexity": PerplexityProvider,
    "reka": RekaProvider,
    "together": TogetherProvider,
    "xai": XAIProvider,
}


def load_provider_by_name(provider_name: str) -> Provider:
    provider = LLM_PROVIDERS[provider_name.lower()]
    return provider()


def load_provider_from_model(model: Model) -> Provider:
    provider_name = model.provider.lower()
    provider = LLM_PROVIDERS[provider_name]
    return provider()
