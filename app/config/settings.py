from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Buddy"
    VERSION: str = "1.0.0"
    ENV: str = "development"  # development | staging | production
    PORT: int = 8000

    LOG_LEVEL: str = "INFO"

    ALLOWED_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
