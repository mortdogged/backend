from pydantic import BaseSettings


class Setting(BaseSettings):
    api_key: str
    enviroment: str = "ENVIROMENT", "dev"


settings = Setting(_env_file=".env")
