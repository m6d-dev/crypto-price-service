from functools import cached_property

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    user: str
    password: str
    name: str
    host: str
    port: int
    external_port: int
    driver: str

    @cached_property
    def url(self) -> str:
        return (
            f"postgresql+{self.driver}://"
            f"{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        )

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
        extra="ignore",
    )


class RedisSettings(BaseSettings):
    host: str
    port: int
    password: str | None = None

    @property
    def broker_url(self) -> str:
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/0"
        return f"redis://{self.host}:{self.port}/0"

    @property
    def backend_url(self) -> str:
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/1"
        return f"redis://{self.host}:{self.port}/1"

    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
        env_file=".env",
        extra="ignore",
    )


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
