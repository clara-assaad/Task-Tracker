import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Application settings loaded from environment variables.
    Falls back to sensible defaults if a variable is not set.
    """
    APP_ENV: str = os.getenv("APP_ENV", "development")
    PORT: int = int(os.getenv("PORT", "8000"))


settings = Settings()