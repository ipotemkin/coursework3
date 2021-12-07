from app.errors import NotFoundError, NoContentError, BadRequestError, DatabaseError, ValidationError


class BasicDAO:
    def __init__(self, session, model, schema, nested_schema=None):
        self.session = session
        self.model = model
        self.schema = schema  # if validation needed while creating/updating a record
        self.nested_schema = nested_schema if nested_schema else schema

    def get_all(self, raise_errors=True):
        objs = self.session.query(self.model).all()
        if raise_errors and not objs:
            raise NotFoundError
        return [self.nested_schema.from_orm(obj).dict() for obj in objs]
        # return objs

    def get_one(self, uid: int):
        if not (obj := self.session.query(self.model).get(uid)):
            raise NotFoundError
        return self.nested_schema.from_orm(obj).dict()
        # return obj

    def create(self, new_obj: dict):
        if not new_obj:
            raise NoContentError

        # to check whether the new_obj meets the model; it will be unnecessary after DB migration
        try:
            self.schema.parse_obj(new_obj)
        except Exception as e:
            # print(f'Error: {e}')
            raise ValidationError

        try:
            obj = self.model(**new_obj)
        except Exception:
            raise BadRequestError

        try:
            self.session.add(obj)
            self.session.commit()
        except Exception as e:
            # print(e)
            raise DatabaseError
        return obj

    def update(self, new_obj: dict, uid: int):
        if not new_obj:
            raise NoContentError

        # excluding None items
        new_obj = {k: v for k, v in new_obj.items() if v is not None}

        # if exists id in new_obj should be equal to uid
        if ('id' in new_obj) and (uid != new_obj['id']):
            raise BadRequestError

        # checking existence of the record
        q = self.session.query(self.model).filter(self.model.id == uid)
        if not q:
            raise NotFoundError

        try:
            q.update(new_obj)
            self.session.commit()
        except Exception:
            raise DatabaseError

    def delete(self, uid: int):
        if not (obj := self.session.query(self.model).get(uid)):
            raise NotFoundError
        try:
            self.session.delete(obj)
            self.session.commit()
        except Exception:
            raise DatabaseError

    def get_all_by_filter(self, req: dict):
        if not (res := self.session.query(self.model).filter_by(**req).all() if req else self.model.query.all()):
            raise NotFoundError
        return [self.nested_schema.from_orm(obj).dict() for obj in res]
