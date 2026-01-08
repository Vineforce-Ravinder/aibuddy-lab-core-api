from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Buddy"
    VERSION: str = "1.0.0"
    ENV: str = "development"  # development | staging | production
    PORT: int = 8000

    LOG_LEVEL: str = "INFO"

    ALLOWED_ORIGINS: list[str] = ["*"]
    
    # Ravinder changed the DB URL for Postgresql connection

    DATABASE_URL:str = 'postgresql://postgres:123456@localhost:5432/aitutorlabdb'

    # Anmol changed the DB URL for Postgresql connection
    # DATABASE_URL: str = "postgresql://postgres:Hunter%40321@localhost:5432/aitutorlabdb"
        

    class Config:
        env_file = ".env"


settings = Settings()
