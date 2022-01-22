from app.dao.basic import BasicDAO
from app.dao.model.users import User, UserBM
from app.constants import ITEMS_ON_PAGE
from app.errors import NotFoundError


class UserDAO(BasicDAO):
    def __init__(self, session, model=User, schema=UserBM):
        super().__init__(session, model, schema)

    def get_all(self, raise_errors=True, page=None, limit=ITEMS_ON_PAGE):
        start_at = 0
        if page is None:
            limit = None
        else:
            start_at = (page - 1) * limit

        objs = self.session.query(self.model).offset(start_at).limit(limit).all()
        # if raise_errors and not objs:
        #     raise NotFoundError
        return [self.nested_schema.from_orm(obj).dict(exclude={"password"}) for obj in objs]

    def get_one(self, uid: int):
        if not (obj := self.session.query(self.model).get(uid)):
            raise NotFoundError
        return self.nested_schema.from_orm(obj).dict(exclude={"password"})
        # return obj

    def get_passwd(self, uid: int):
        if not (obj := self.session.query(self.model).get(uid)):
            raise NotFoundError
        return obj.password
        # return self.nested_schema.from_orm(obj).dict(exclude={"password"})
        # return obj
