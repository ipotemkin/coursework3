from app.dao.basic import BasicDAO
from app.dao.model.users import User, UserBM


class UserDAO(BasicDAO):
    def __init__(self, session, model=User, schema=UserBM):
        super().__init__(session, model, schema)
