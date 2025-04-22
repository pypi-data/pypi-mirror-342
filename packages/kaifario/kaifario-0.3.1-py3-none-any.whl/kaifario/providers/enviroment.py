import os
from typing import Any

from kaifario.protocols import ConfigurationProvider


class EnviromentProvider(ConfigurationProvider):
    def __init__(
        self,
        prefix: str = "",
        separator: str = "__",
    ) -> None:
        self.prefix = prefix.lower()
        self.separator = separator

    def _set_nested_value(
        self,
        data: dict[str, Any],
        keys: list[str],
        value: Any,
    ) -> None:
        current = data
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value

    def load(self) -> dict[str, Any]:
        data: dict[str, Any] = {}
        for env, value in os.environ.items():
            env = env.lower()
            s = env
            if self.prefix:
                if env.startswith(self.prefix):
                    s = env.removeprefix(self.prefix)
                else:
                    continue
            keys = s.split(self.separator)
            self._set_nested_value(data, keys, value)
        return data
