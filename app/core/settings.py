from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()
class Settings(BaseModel):
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = os.getenv('ALGORITHM')
    ACCESS_TOKEN_MINUTES: int = int(os.getenv("ACCESS_TOKEN_MINUTES"))
    REFRESH_TOKEN_DAYS: int = int(os.getenv("REFRESH_TOKEN_DAYS"))
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()

