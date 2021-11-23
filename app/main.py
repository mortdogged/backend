from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from app.api import profile


def create_application() -> FastAPI:
    middleware = [
        Middleware(CORSMiddleware, allow_origins=["https://www.mortdogged.com"])
    ]

    application = FastAPI(middleware=middleware)
    application.include_router(profile.router, prefix="/profile", tags=["profile"])

    return application


app = create_application()
