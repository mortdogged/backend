import redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routers import profile


def create_application() -> FastAPI:
    application = FastAPI()
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["https://mortdogged.com"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(profile.router, prefix="/profile", tags=["profile"])

    return application


client_redis = redis.Redis.from_url(get_settings().redis_url)
client_redis.set("nombre", "alvaro", ex=60)
test = client_redis.get("nombre")
print(test)


app = create_application()
