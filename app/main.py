from fastapi import FastAPI


def create_application() -> FastAPI:
    application = FastAPI()

    @application.get("/ping")
    async def pong():
        return {"ping": "pong!"}

    return application


app = create_application()
