from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


app = create_application()
