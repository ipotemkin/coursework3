from app.dao.basic import BasicDAO
from app.dao.model.rtokens import RToken, RTokenBM


class RTokenDAO(BasicDAO):
    def __init__(self, session, model=RToken, schema=RTokenBM):
        super().__init__(session, model, schema)
