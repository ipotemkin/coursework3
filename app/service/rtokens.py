from app.service.basic import BasicService
from app.dao.rtokens import RTokenDAO
import jwt
from app.constants import JWT_KEY, JWT_METHOD


class RTokenService(BasicService):
    def __init__(self, session):
        super().__init__(RTokenDAO(session))

    def del_expired(self):
        tokens = self.dao.get_all(raise_errors=False)
        for token in tokens:
            try:
                jwt.decode(token["token"], JWT_KEY, [JWT_METHOD])
            except Exception as e:
                print(f"Token with ID={token['id']} status {e}")
                self.dao.delete(token["id"])
