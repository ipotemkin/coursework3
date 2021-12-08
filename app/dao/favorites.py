from app.dao.basic import BasicDAO
from app.dao.model.favotites import FavoriteMovie, FavoriteMovieBM


class FavoriteMovieDAO(BasicDAO):
    def __init__(self, session, model=FavoriteMovie, schema=FavoriteMovieBM):
        super().__init__(session, model, schema)
