from app.dao.basic import BasicDAO
from app.dao.model.genres import Genre, GenreBM


class GenreDAO(BasicDAO):
    def __init__(self, session, model=Genre, schema=GenreBM):
        super().__init__(session, model, schema)
