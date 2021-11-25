import logging
from functools import lru_cache

import redis
from pydantic import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    api_key: str
    environment: str = "dev"
    redis_url: str
    cache_expired_time: int = 60 * 10


@lru_cache
def get_settings() -> Settings:
    log.info("Loading config settings from the environment...")
    settings = Settings(_env_file="./.env")
    return settings


@lru_cache
def get_cache():
    return redis.Redis.from_url(get_settings().redis_url)
