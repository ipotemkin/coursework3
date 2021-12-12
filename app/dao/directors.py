from app.dao.basic import BasicDAO
from app.dao.model.directors import Director, DirectorBM


class DirectorDAO(BasicDAO):
    def __init__(self, session, model=Director, schema=DirectorBM):
        super().__init__(session, model, schema)

    def __repr__(self):
        return f"<DirectorDAO (model={self.model})>"
