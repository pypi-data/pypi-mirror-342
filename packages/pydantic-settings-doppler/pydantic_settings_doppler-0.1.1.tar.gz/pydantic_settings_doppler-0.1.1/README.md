# Pydantic Settings Doppler

[![CI](https://github.com/ajauniskis/pydantic-settings-doppler/actions/workflows/test.yaml/badge.svg)](https://github.com/ajauniskis/pydantic-settings-doppler/actions/workflows/test.yaml)
[![codecov](https://codecov.io/gh/ajauniskis/pydantic-settings-doppler/graph/badge.svg?token=XB1M3ET2H7)](https://codecov.io/gh/ajauniskis/pydantic-settings-doppler)
[![Pydantic v2 only](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://docs.pydantic.dev/latest/contributing/#badges)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/pydantic-settings-doppler)](https://pypi.org/project/pydantic-settings-doppler)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydantic-settings-doppler)](https://pypi.org/project/pydantic-settings-doppler)
[![PyPI - License](https://img.shields.io/pypi/l/pydantic-settings-doppler)](https://pypi.org/project/pydantic-settings-doppler)
![PyPI - Version](https://img.shields.io/pypi/v/pydantic-settings-doppler)


Pydantic Settings for Doppler integration! This package provides a seamless way to load configuration values from [Doppler](https://www.doppler.com/) into your Pydantic models. It leverages the power of Doppler's secrets management and Pydantic's settings management to make your application configuration secure and easy to use.

## 🚀 Features

- **Secure**: Fetch secrets directly from Doppler.
- **Simple**: Integrates seamlessly with Pydantic's `BaseSettings`.
- **Flexible**: Supports environment variable fallbacks and default values.

## 📦 Installation

Install the package using `pip`:

```bash
pip install pydantic-settings-doppler
```

## 🛠️ Usage

Here's a quick example to get you started:

```python
from pydantic_settings import BaseSettings
from pydantic_settings.sources import PydanticBaseSettingsSource
from pydantic_settings_doppler import DopplerSettingsSource


class Settings(BaseSettings):
    database_url: str
    api_key: str

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            DopplerSettingsSource(
                settings_cls,
                token="your-doppler-token",
                project_id="your-project-id",
                config_id="your-config-id",
            ),
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


# Load settings
settings = Settings()
print(settings.database_url)
print(settings.api_key)

```

## 📖 Documentation

For more details, check out the [Doppler documentation](https://www.doppler.com/docs) and [Pydantic documentation](https://docs.pydantic.dev/).

## 🧑‍💻 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## ⚖️ License

This project is licensed under the [MIT License](./LICENSE).
