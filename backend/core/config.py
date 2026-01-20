from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # База данных
    DATABASE_URL: str = "sqlite:///./app.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
