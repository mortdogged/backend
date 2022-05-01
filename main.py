import uvicorn
from app.main import app  # noqa / for Deta.sh

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
