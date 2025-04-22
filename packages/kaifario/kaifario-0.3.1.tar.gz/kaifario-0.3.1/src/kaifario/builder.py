from typing import Any, Self

from kaifario.configuration import Configuration
from kaifario.protocols.provider import ConfigurationProvider


class ConfigurationBuilder:
    _providers: list[ConfigurationProvider]

    def __init__(self) -> None:
        self._providers = []

    def add_provider(self, provider: ConfigurationProvider) -> Self:
        self._providers.append(provider)
        return self

    def add_providers(self, *providers: ConfigurationProvider) -> Self:
        self._providers.extend(providers)
        return self

    def build(self) -> Configuration:
        data: dict[str, Any] = {}
        for provider in self._providers:
            _deep_merge(data, provider.load())
        self._providers = []
        return Configuration(data)


def _deep_merge(
    dest: dict[str, Any],
    source: dict[str, Any],
) -> dict[str, Any]:
    for key, value in source.items():
        if (
            key in dest
            and isinstance(dest[key], dict)
            and isinstance(value, dict)
        ):
            dest[key] = _deep_merge(dest[key], value)
        else:
            dest[key] = value
    return dest
