import os

from kaifario.providers.enviroment import EnviromentProvider


def test_envirmonent_provider() -> None:
    os.environ["TEST_KEY1"] = "test_value1"
    os.environ["TEST_KEY2__KEY"] = "test_value2"

    provider = EnviromentProvider(prefix="TEST_")
    data = provider.load()

    del os.environ["TEST_KEY1"]
    del os.environ["TEST_KEY2__KEY"]

    assert data["key1"] == "test_value1"
    assert data["key2"]["key"] == "test_value2"


def test_envirmonent_provider_empty() -> None:
    provider = EnviromentProvider(prefix="TEST_")
    data = provider.load()

    assert data == {}
