from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import profile


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(profile.router, prefix="/profile", tags=["profile"])

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["https://www.mortdogged.com"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = create_application()
