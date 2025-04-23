import os
from typing import Any, Dict, Optional

from dopplersdk import DopplerSDK
from pydantic.fields import FieldInfo
from pydantic_settings import PydanticBaseSettingsSource
from pydantic_settings.sources import SettingsError

from pydantic_settings_doppler.logger import logger


class DopplerSettingsSource(PydanticBaseSettingsSource):
    """
    A source for settings that retrieves values from Doppler.
    """

    def __init__(
        self,
        settings_cls: type,
        token: Optional[str] = None,
        project_id: Optional[str] = None,
        config_id: Optional[str] = None,
    ) -> None:
        super().__init__(settings_cls)
        self._client = self._initialize_client(token)
        self._project_id = self._get_required_value(
            project_id, "DOPPLER_PROJECT_ID", "Doppler project ID"
        )
        self._config_id = self._get_required_value(
            config_id, "DOPPLER_CONFIG_ID", "Doppler config ID"
        )

    def __call__(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(
                field, field_name
            )
            field_value = self.prepare_field_value(
                field_name, field, field_value, value_is_complex
            )
            if field_value is not None:
                d[field_key] = field_value

        return d

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> tuple[Any, str, bool]:
        logger.debug(f"Getting {field_name} value from Doppler")

        name = field.alias or field.serialization_alias or field_name

        secret = self._client.secrets.get(
            project=self._project_id,
            config=self._config_id,
            name=name.upper(),
        )
        field_value = self._extract_secret_value(secret)

        if field_value is None:
            if field.is_required():
                logger.warning(f"{field_name} not found in Doppler")
                raise SettingsError(f"{field_name} not found in Doppler")
            field_value = field.default

        return field_value, field_name, False

    def _initialize_client(self, token: Optional[str]) -> DopplerSDK:
        token = self._get_required_value(token, "DOPPLER_TOKEN", "Doppler access token")
        return DopplerSDK(access_token=token)

    def _get_required_value(
        self, value: Optional[str], env_var: str, description: str
    ) -> str:
        result = value or os.environ.get(env_var)
        if not result:
            raise SettingsError(f"{description} is required but not provided.")
        return result

    def _extract_secret_value(self, secret: Any) -> Any:
        return (
            secret.value.get("raw")  # pyright: ignore[reportAttributeAccessIssue]
            if secret
            else None
        )
