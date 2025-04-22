import json
from typing import Any

from kaifario.protocols import ConfigurationProvider


class JsonProvider(ConfigurationProvider):
    def __init__(self, path: str) -> None:
        self.path = path

    def load(self) -> dict[str, Any]:
        with open(self.path) as f:
            return json.load(f)
