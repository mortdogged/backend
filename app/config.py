import logging
from functools import cache

from pydantic import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    api_key: str
    environment: str = "dev"


@cache
def get_settings() -> Settings:
    log.info("Loading config settings from the environment...")
    return Settings()
