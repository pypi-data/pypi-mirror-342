from typing import Any, Protocol


class ConfigurationProvider(Protocol):
    def load(self) -> dict[str, Any]: ...
