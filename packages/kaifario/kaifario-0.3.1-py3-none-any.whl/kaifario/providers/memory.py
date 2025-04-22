from typing import Any

from kaifario.protocols import ConfigurationProvider


class MemoryProvider(ConfigurationProvider):
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def load(self) -> dict[str, Any]:
        return self.data
