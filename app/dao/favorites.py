from app.dao.basic import BasicDAO
from app.dao.model.favorites import FavoriteMovie, FavoriteMovieBM


class FavoriteMovieDAO(BasicDAO):
    def __init__(self, session, model=FavoriteMovie, schema=FavoriteMovieBM):
        super().__init__(session, model, schema)
