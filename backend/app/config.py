from pathlib import Path
from typing import ClassVar, Optional
from urllib.parse import quote_plus

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


def _sanitize_mongodb_uri(uri: str) -> str:
    """Normalize MongoDB URI credentials if the password contains reserved chars."""
    if not uri:
        return uri
    if not (uri.startswith('mongodb://') or uri.startswith('mongodb+srv://')):
        return uri

    scheme, rest = uri.split('://', 1)
    if '@' not in rest:
        return uri

    # Preserve the rightmost @ as the separator between auth and host.
    userinfo, hostinfo = rest.rsplit('@', 1)
    if ':' not in userinfo:
        return uri

    username, password = userinfo.split(':', 1)
    safe_username = quote_plus(username)
    safe_password = quote_plus(password)
    return f"{scheme}://{safe_username}:{safe_password}@{hostinfo}"


class Settings(BaseSettings):
    project_root: ClassVar[Path] = Path(__file__).resolve().parent.parent
    model_config = SettingsConfigDict(env_file=project_root / ".env", case_sensitive=True)

    # MongoDB connection URI (Atlas or local). Do NOT hardcode credentials.
    MONGODB_URI: SecretStr = Field(default_factory=lambda: SecretStr("mongodb://localhost:27017"))

    # Database name to use in MongoDB
    DATABASE_NAME: str = Field("iot_trust_db")

    # MQTT broker settings
    MQTT_BROKER: str = Field("localhost")
    MQTT_PORT: int = Field(1883)
    MQTT_USERNAME: Optional[str] = Field(None)
    MQTT_PASSWORD: Optional[SecretStr] = Field(None)
    MQTT_TOPIC: str = Field("iot/devices/data")

    @property
    def mongodb_uri(self) -> str:
        return _sanitize_mongodb_uri(self.MONGODB_URI.get_secret_value())


settings = Settings()
