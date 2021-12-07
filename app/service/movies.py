from app.service.basic import BasicService
from app.dao.movies import MovieDAO


class MovieService(BasicService):
    def __init__(self, session):
        super().__init__(MovieDAO(session))
