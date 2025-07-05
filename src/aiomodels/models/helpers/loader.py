from aiomodels.models.model import Model


def load_model_by_name(model_name: str) -> Model:
    provider_name, model_name = model_name.split(":", 1)
    return Model(id=model_name, name=model_name, provider=provider_name)
