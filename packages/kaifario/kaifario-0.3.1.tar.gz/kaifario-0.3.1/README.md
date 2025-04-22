# Kaifario

**Kaifario** is a lightweight and flexible configuration builder library for Python, inspired by the builder-style configuration system from C#. It allows you to compose multiple configuration sources (memory, environment variables, files, etc.) into a single, unified configuration object.

## 🔧 Installation

```bash
pip install kaifario
```

## 🚀 Quick Start

```python
from kaifario.builder import ConfigurationBuilder
from kaifario.providers.memory import MemoryProvider

config = ConfigurationBuilder().add_providers(
    MemoryProvider({"a": 1, "b": 2})
).build()

print(config.get_value("a", int))  # Output: 1
```

## 📦 Available Providers

Kaifario supports various configuration sources:

- `MemoryProvider` — Load configuration from a Python dictionary.
- `EnviromentProvider` — Load values from environment variables, with support for nested configuration structures using a prefix and separator. Environment variable keys are lowercased and split by the given separator (default is `"__"`) to create nested dictionaries. For example:

  ```bash
  export APP_DATABASE__HOST=localhost
  export APP_DATABASE__PORT=5432
  ```

  With `EnviromentProvider(prefix="APP_")`, this would produce:

  ```python
  {
      "database": {
          "host": "localhost",
          "port": "5432"
      }
  }
  ```

- `IniProvider` — Load from `.ini` files.
- `JsonProvider` — Load from JSON files.
- `TomlProvider` — Load from TOML files.
- `YamlProvider` — Load from YAML files.

### Provider Merge Order

When using multiple providers, their configurations are **merged** into a single dictionary. Later providers **override** the values from earlier ones if keys conflict. This allows flexible layering of configuration sources, such as defaults overridden by environment variables.

### Example with multiple providers

```python
from kaifario.builder import ConfigurationBuilder
from kaifario.providers.env import EnviromentProvider
from kaifario.providers.json import JsonProvider
from kaifario.providers.memory import MemoryProvider

config = ConfigurationBuilder() \
    .add_providers(
        EnviromentProvider(prefix="APP"),
        JsonProvider("config.json"),
        MemoryProvider({"fallback": "value"})
    ) \
    .build()

print(config["database"].get_value("host", str))
# or config.get_section("database").get_value("host", str)
```

## 🧹 Custom Providers

You can define your own provider by implementing the `ConfigurationProvider` protocol:

```python
from typing import Protocol, Any

class ConfigurationProvider(Protocol):
    def load(self) -> dict[str, Any]:
        ...
```

### Example

```python
class CustomProvider:
    def load(self) -> dict[str, Any]:
        return {"custom_key": "custom_value"}
```

Then use it just like any other provider:

```python
config = ConfigurationBuilder().add_providers(CustomProvider()).build()
print(config.get_value("custom_key", str))
```

## 📊 Dataclass Mapping

Kaifario supports direct mapping of configuration data to Python dataclasses. Under the hood, it uses [Retort](https://github.com/reagento/adaptix), but you can also provide your own loader by implementing a custom `Loader`.

### Usage Example

```python
from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    host: str
    port: int

config = ConfigurationBuilder().add_providers(...).build() # inner config data should contain {"host": ..., "port": ...}
db_config = config.get(DatabaseConfig)

# with nested data like {"database": {"host": ..., "port": ...}} you can use:
db_config = config['database'].get(DatabaseConfig)
```
### Custom Loader Support

You can provide your own loader by implementing the following protocol:

```python
class Loader(Protocol):
    def load(self, data: dict[str, Any], model: type[T]) -> T:
        ...
```

The `Configuration` class accepts an optional `loader` argument:

## 🤝 Contributing

Contributions, ideas, and bug reports are welcome! Feel free to open issues or submit pull requests.

## 📃 License

MIT License
