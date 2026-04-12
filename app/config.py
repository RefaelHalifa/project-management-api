from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str

    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # App info
    app_name: str = "Project Management API"
    app_version: str = "1.0.0"

    class Config:
        # Tells Pydantic: read values from the .env file
        env_file = ".env"

# One single instance imported everywhere in the app
settings = Settings()