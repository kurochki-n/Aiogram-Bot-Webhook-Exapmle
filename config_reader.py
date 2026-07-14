from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    BOT_TOKEN: SecretStr
    CHANNEL_ID: int

    WEBHOOK_PORT: int
    WEBHOOK_URL: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Config()
