import os

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Inventory API")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./inventory.db")

settings = Settings()
