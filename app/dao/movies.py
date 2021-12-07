from app.dao.basic import BasicDAO
from app.dao.model.movies import Movie, MovieBM, MovieBMSimple


class MovieDAO(BasicDAO):
    def __init__(self, session, model=Movie, schema=MovieBMSimple, nested_schema=MovieBM):
        super().__init__(session, model, schema, nested_schema)
