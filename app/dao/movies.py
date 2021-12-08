from app.dao.basic import BasicDAO
from app.dao.model.movies import Movie, MovieBM, MovieBMSimple
from app.constants import ITEMS_ON_PAGE
from app.errors import NotFoundError
from sqlalchemy import desc


class MovieDAO(BasicDAO):
    def __init__(self, session, model=Movie, schema=MovieBMSimple, nested_schema=MovieBM):
        super().__init__(session, model, schema)  # , nested_schema)

    def get_all(self, raise_errors=True, page=None, limit=ITEMS_ON_PAGE, state=None):
        start_at = 0
        if page is None:
            limit = None
        else:
            start_at = (page - 1) * limit

        if state == 'new':
            objs = self.session.query(self.model).order_by(desc('year')).offset(start_at).limit(limit).all()
        else:
            objs = self.session.query(self.model).offset(start_at).limit(limit).all()

        if raise_errors and not objs:
            raise NotFoundError
        return [self.nested_schema.from_orm(obj).dict() for obj in objs]
        # return objs

    def get_all_by_filter(self, req: dict, page=None, limit=ITEMS_ON_PAGE, state=None):
        start_at = 0
        if page is None:
            limit = None
        else:
            start_at = (page - 1) * limit

        if state == 'new':
            if req:
                res = self.session.query(self.model).filter_by(**req).order_by(desc('year')).limit(limit).offset(start_at).all()
            else:
                res = self.model.query.order_by(desc('year')).offest(start_at).limit(limit).all()

        else:
            if req:
                res = self.session.query(self.model).filter_by(**req).limit(limit).offset(start_at).all()
            else:
                res = self.model.query.offest(start_at).limit(limit).all()

        if not res:
            raise NotFoundError

        # if not (res := self.session.query(self.model).filter_by(**req).offest(start_at).limit(limit).all() if req else self.model.query.all()):
        #     raise NotFoundError

        return [self.nested_schema.from_orm(obj).dict() for obj in res]

