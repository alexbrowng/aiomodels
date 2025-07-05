import abc


class JsonSchemaType(abc.ABC):
    """Json schema type."""

    @abc.abstractmethod
    def to_primitives(self) -> dict:
        pass
