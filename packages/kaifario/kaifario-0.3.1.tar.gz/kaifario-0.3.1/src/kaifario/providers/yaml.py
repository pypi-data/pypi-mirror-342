from typing import Any

import yaml

from kaifario.protocols import ConfigurationProvider


class YamlProvider(ConfigurationProvider):
    def __init__(self, path: str) -> None:
        self.path = path

    def load(self) -> dict[str, Any]:
        with open(self.path) as f:
            return yaml.safe_load(f)
