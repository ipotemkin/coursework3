from pydantic import BaseSettings
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Settings(BaseSettings):
    jwt_key: str = "test"
    pwd_hash_salt: bytes = b"test_salt"


settings = Settings()
