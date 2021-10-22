from fastapi import FastAPI
from config import settings


def create_application() -> FastAPI:
    application = FastAPI()

    @application.get("/ping")
    async def pong():
        return {"ping": "pong!"}

    return application


app = create_application()
