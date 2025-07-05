import pytest
from aiomodels.parameters.parameters import Parameters


def test_parameters_defaults():
    params = Parameters()
    assert params.max_tokens is None
    assert params.temperature is None
    assert params.top_p is None
    assert params.frequency_penalty is None
    assert params.presence_penalty is None
    assert params.stop is None


def test_parameters_custom():
    params = Parameters(
        max_tokens=100, temperature=0.5, top_p=0.9, frequency_penalty=0.1, presence_penalty=0.2, stop=["END"]
    )
    assert params.max_tokens == 100
    assert params.temperature == pytest.approx(0.5)
    assert params.top_p == pytest.approx(0.9)
    assert params.frequency_penalty == pytest.approx(0.1)
    assert params.presence_penalty == pytest.approx(0.2)
    assert params.stop == ["END"]
