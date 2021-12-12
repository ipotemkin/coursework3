from dotenv import load_dotenv
import os

# try:
#     load_dotenv()
# except:
#     pass

load_dotenv()

PWD_HASH_SALT = os.getenv('PWD_HASH_SALT')
JWT_KEY = os.getenv('JWT_KEY')

# PWD_HASH_SALT = b'the highest secret possible'
# JWT_KEY = 'SkyPro2021!'

PWD_HASH_ITERATIONS = 100_000
AC_TOKEN_EXP_TIME_MIN = 30
R_TOKEN_EXP_TIME_DAYS = 1
JWT_METHOD = 'HS256'
ITEMS_ON_PAGE = 2
