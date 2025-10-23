import os
from dotenv import load_dotenv
from pydantic import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    BOT_TOKEN: str
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite+aiosqlite:///./data/db.sqlite')


    class Config:
        env_file = '.env'


settings = Settings()