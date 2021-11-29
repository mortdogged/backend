from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from .consts import DESCRIPTION
from .routers import matches, profile


def create_application() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://mortdogged.com"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(profile.router, prefix="/profile", tags=["profile"])
    app.include_router(matches.router, prefix="/matches", tags=["matches"])

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="MORTDOGGED API",
            version="0.0.1",
            description=DESCRIPTION,
            routes=app.routes,
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
    return app


app = create_application()
