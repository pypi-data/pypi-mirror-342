from dataclasses import dataclass

from kaifario.builder import ConfigurationBuilder
from kaifario.providers.memory import MemoryProvider


def test_configration() -> None:
    config = (
        ConfigurationBuilder()
        .add_providers(
            MemoryProvider({"a": "a1", "b": "b1"}),
            MemoryProvider({"a": "a2"}),
        )
        .build()
    )

    assert config.get_value("a", str) == "a2"
    assert config.get_value("b", str) == "b1"


def test_configration_mapping() -> None:
    config = (
        ConfigurationBuilder()
        .add_providers(
            MemoryProvider({"test": {"b": "b1", "a": 5, "c": [1, 2, 3]}}),
        )
        .build()
    )

    @dataclass
    class TestConfig:
        b: str
        a: int
        c: list[int]

    test_config = config["test"].get(TestConfig)

    assert test_config.b == "b1"
    assert test_config.a == 5
    assert test_config.c == [1, 2, 3]
