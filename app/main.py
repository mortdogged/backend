from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from .consts import DESCRIPTION
from .exceptions import InvalidAPIKeyException, SummonerNotFoundException
from .routers import profile


def create_application() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://mortdogged.com"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(profile.router, prefix="/profile", tags=["profile"])

    @app.exception_handler(SummonerNotFoundException)
    async def summoner_not_found_exception_handler(request, exc):
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND, content={"detail": "Summoner not found"}
        )

    @app.exception_handler(InvalidAPIKeyException)
    async def invalid_api_key_exception_handler(request, exc):
        return JSONResponse(
            status_code=HTTPStatus.BAD_GATEWAY, content={"detail": "Invalid API Key"}
        )

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="MORTDOGGED API",
            version="0.0.2",
            description=DESCRIPTION,
            routes=app.routes,
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
    return app


app = create_application()
