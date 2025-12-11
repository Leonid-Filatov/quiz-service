import os

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://quiz_user:quiz_password@postgres:5432/quiz_db")

settings = Settings()