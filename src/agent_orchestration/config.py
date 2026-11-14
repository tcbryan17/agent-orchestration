"""Runtime settings, read from the environment (and a local `.env` file, which is gitignored)."""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Optional so tests and CI run without a key. Code that calls the API must fail fast when
    # it is None. SecretStr keeps the value out of logs and reprs; call .get_secret_value()
    # only at the point of use.
    anthropic_api_key: SecretStr | None = None

    # Haiku-first policy (docs/decisions/0002): every agent starts on Haiku and is upgraded
    # individually only when an eval shows the cheaper model is the bottleneck.
    default_model: str = "claude-haiku-5-5"


settings = Settings()
