from app.config import settings
from os import environ

JWT_KEY = settings.jwt_key
PWD_HASH_SALT = settings.pwd_hash_salt

PWD_HASH_ITERATIONS = 100_000
AC_TOKEN_EXP_TIME_MIN = 30
R_TOKEN_EXP_TIME_DAYS = 1
JWT_METHOD = "HS256"
ITEMS_ON_PAGE = 2
RATE_LIMIT_PER_SECOND = 1
NO_RATE_LIMIT = environ.get("NO_RATE_LIMIT")
