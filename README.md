Coursework 3 on Fast API
=======

Usage
------

Please look at the SWAGGER welcome page

Authorization rules:
-----

To use some endpoints you need authorization.

Please sign up through Swagger or /auth/login.

You have to give your email (will be your login) and password.

After authorization, you will get two tokens:
- access token valid during 30 minutes and
- refresh token valid during 1 day

You can use your pair of tokens only once to get a new pair of tokens


Testing data
------

You can find testing data in fixtures.py

To build up a database with these testing data just run create_data.py

Dependencies
-------

This projects uses an ultra-fast library ujson to read jsons

1. SQLAlchemy
2. PyDantic
3. PyJWT
4. FastAPI
5. uvicorn
6. fastapi_utils
7. python-multipart
8. email-validator
9. python-dotenv
10. ujson
11. types-ujson
