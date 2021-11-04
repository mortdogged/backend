from fastapi import FastAPI

from app.api import profile


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(profile.router, prefix="/profile", tags=["profile"])

    return application


app = create_application()
