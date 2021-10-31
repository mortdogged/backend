import logging
from functools import lru_cache

from pydantic import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    api_key: str
    environment: str = "dev"


@lru_cache
def get_settings() -> Settings:
    log.info("Loading config settings from the environment...")
    return Settings()
