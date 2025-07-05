import pytest
from aiomodels.models.model import Model, ModelPrice


def test_model_creation_minimal():
    model = Model(id="gpt-4o-mini", name="GPT 4o mini", provider="OpenAI")
    assert model.id == "gpt-4o-mini"
    assert model.name == "GPT 4o mini"
    assert model.provider == "OpenAI"
    assert model.price is None


def test_model_creation_with_prices():
    model = Model(id="gpt-4o", name="GPT 4o", provider="OpenAI", price=ModelPrice(input=0.01, output=0.02))
    assert model.price is not None
    assert model.price.input == pytest.approx(0.01)
    assert model.price.output == pytest.approx(0.02)
