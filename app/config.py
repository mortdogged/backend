import logging
from functools import lru_cache

import redis
from pydantic import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    api_key: str
    environment: str = "dev"
    redis_url: str = None
    cache_expired_time: int = 60 * 10


class CacheService:
    def __init__(self, redis_client=None):
        self.redis_client = redis_client

    def get(self, *args, **kwargs):
        if self.redis_client:
            return self.redis_client.get(*args, **kwargs)
        return None

    def set(self, *args, **kwargs):
        if self.redis_client:
            return self.redis_client.set(*args, **kwargs)


@lru_cache
def get_settings() -> Settings:
    log.info("Loading config settings from the environment...")
    settings = Settings(_env_file="./.env")
    return settings


@lru_cache
def get_cache():
    redis_url = get_settings().redis_url
    if not redis_url:
        return CacheService()
    return CacheService(redis.Redis.from_url(redis_url))
