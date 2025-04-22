import configparser
from typing import Any

from kaifario.protocols import ConfigurationProvider


class IniProvider(ConfigurationProvider):
    def __init__(self, path: str) -> None:
        self.path = path

    def load(self) -> dict[str, Any]:
        config = configparser.ConfigParser()
        config.read(self.path)
        config_dict: dict[str, Any] = {
            section: dict(config.items(section))
            for section in config.sections()
        }
        return config_dict
