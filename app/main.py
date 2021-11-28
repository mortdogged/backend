from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

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


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="MORTDOGGED API",
        version="0.0.1",
        description="mortdogged.com isn't endorsed by Riot Games and doesn't reflect "
        "the views or opinions of Riot Games or anyone officially involved in "
        "producing or managing Riot Games properties. Riot Games, "
        "and all associated properties are trademarks or registered "
        "trademarks of Riot Games, Inc.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
