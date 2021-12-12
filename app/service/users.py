import hashlib
import hmac

from fastapi import HTTPException, status

import jwt
from app.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from app.constants import (
    JWT_KEY,
    JWT_METHOD,
    AC_TOKEN_EXP_TIME_MIN,
    R_TOKEN_EXP_TIME_DAYS,
)

from app.service.basic import BasicService
from app.dao.users import UserDAO
from app.dao.model.rtokens import UserForTokenModel, TokenModel

import datetime
import calendar

from app.service.rtokens import RTokenService


class UserService(BasicService):
    def __init__(self, session):
        super().__init__(UserDAO(session))

    @staticmethod
    def get_hash(password):
        return hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS,
        ).decode("utf-8", "ignore")

    # @staticmethod
    # def gen_token(data):
    #     access_token = jwt.encode(data, 's3cR$eT', 'HS256')
    #     return access_token

    @staticmethod
    def check_access_token(access_token: str) -> TokenModel:
        try:
            data = jwt.decode(access_token, JWT_KEY, [JWT_METHOD])
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"JWT Exception Error: {e}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return TokenModel.parse_obj(data)

    def check_refresh_token(self, refresh_token: str):
        token = RTokenService(self.dao.session).get_all_by_filter(
            {"token": refresh_token}
        )
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token is already used or invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )

        RTokenService(self.dao.session).delete(token[0]["id"])
        return self.check_access_token(refresh_token)

    def gen_jwt(self, user_obj: dict):
        UserForTokenModel.parse_obj(user_obj)  # to validate the model

        t0 = datetime.datetime.utcnow()

        ends_at = t0 + datetime.timedelta(minutes=AC_TOKEN_EXP_TIME_MIN)
        user_obj["exp"] = calendar.timegm(ends_at.timetuple())
        access_token = jwt.encode(user_obj, JWT_KEY, JWT_METHOD)

        ends_at = t0 + datetime.timedelta(days=R_TOKEN_EXP_TIME_DAYS)
        user_obj["exp"] = calendar.timegm(ends_at.timetuple())
        refresh_token = jwt.encode(user_obj, JWT_KEY, JWT_METHOD)

        RTokenService(self.dao.session).create({"token": refresh_token})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    def refresh_jwt(self, refresh_token: str):
        data = jwt.decode(refresh_token, JWT_KEY, [JWT_METHOD])
        return self.gen_jwt(data)

    def check_password(self, email: str, password: str) -> bool:
        """
        Checks a user's password
        :param email: user login name
        :param password: a password to check
        :return: True or False
        """
        password_hash = self.get_hash(password)
        user_password = self.dao.get_all_by_filter({"email": email})[0]["password"]
        return hmac.compare_digest(
            password_hash.encode("utf-8"), user_password.encode("utf-8")
        )

    def check_password_with_hash(self, user_password: str, password_hash: str) -> bool:
        """
        Compares a user's password with its hash in the database
        :param user_password: a user password (a decoded string)
        :param password_hash: a hashed password from the user record
        :return: True or False
        """
        user_password_hash = self.get_hash(user_password)
        return hmac.compare_digest(
            password_hash.encode("utf-8"), user_password_hash.encode("utf-8")
        )

    def create(self, new_obj: dict):
        if "password" in new_obj:
            new_obj["password"] = self.get_hash(new_obj["password"])
        return super().create(new_obj)

    def update(self, new_obj: dict, uid: int):
        if ("password" in new_obj) and new_obj["password"] is not None:
            new_obj["password"] = self.get_hash(new_obj["password"])
        return super().update(new_obj, uid)  # TODO

    def update_password(self, pk, old_password: str, new_password: str):
        user = self.dao.get_one(pk)
        if not self.check_password_with_hash(old_password, user.get("password")):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password",
                # headers={"WWW-Authenticate": "Bearer"},
            )
        self.update({"password": new_password}, pk)
