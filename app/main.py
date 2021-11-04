import uvicorn
from fastapi import FastAPI

from app.api import profile


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(profile.router, prefix="/profile", tags=["profile"])

    return application


app = create_application()

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
