import dataclasses

from aiomodels.models.model_price import ModelPrice


@dataclasses.dataclass
class Model:
    id: str
    name: str
    provider: str
    price: ModelPrice | None = None
