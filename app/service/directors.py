from app.service.basic import BasicService
from app.dao.directors import DirectorDAO


class DirectorService(BasicService):
    def __init__(self, session):
        super().__init__(DirectorDAO(session))
