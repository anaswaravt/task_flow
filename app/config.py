from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    #  DATABASE
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./taskflow.db"

    #  JWT
    SECRET_KEY: str = "1eac998eaf7eb54a662eb3ccef54c946"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()