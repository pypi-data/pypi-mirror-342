from typing import Any, Protocol, TypeVar

T = TypeVar("T")


class Loader(Protocol):
    def load(self, data: dict[str, Any], model: type[T]) -> T: ...
