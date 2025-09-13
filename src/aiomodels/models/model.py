import dataclasses
import typing

from aiomodels.models.model_price import ModelPrice


@dataclasses.dataclass
class Model:
    id: str
    name: str
    provider: str
    price: ModelPrice | None = None
    type: typing.Literal["model"] = "model"

    def __str__(self) -> str:
        return f"Model(id={self.id}, name={self.name}, provider={self.provider}, price={self.price})"
