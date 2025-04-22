import tomllib
from typing import Any

from kaifario.protocols import ConfigurationProvider


class TomlProvider(ConfigurationProvider):
    def __init__(self, path: str) -> None:
        self.path = path

    def load(self) -> dict[str, Any]:
        with open(self.path, "rb") as f:
            return tomllib.load(f)
