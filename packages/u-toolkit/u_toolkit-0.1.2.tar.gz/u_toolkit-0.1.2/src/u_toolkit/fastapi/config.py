from pydantic_settings import BaseSettings, SettingsConfigDict


class FastAPISettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="FASTAPI_",
        env_file=(".env", ".env.prod", ".env.dev", ".env.test"),
        extra="ignore",
    )
