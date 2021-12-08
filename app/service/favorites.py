from app.service.basic import BasicService
from app.dao.favorites import FavoriteMovieDAO


class FavoriteMovieService(BasicService):
    def __init__(self, session):
        super().__init__(FavoriteMovieDAO(session))
