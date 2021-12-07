from app.service.basic import BasicService
from app.dao.genres import GenreDAO


class GenreService(BasicService):
    def __init__(self, session):
        super().__init__(GenreDAO(session))
