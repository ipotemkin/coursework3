import pytest
import os
from sqlalchemy.orm import sessionmaker

# from app.dao.model.directors import Director
# from app.dao.model.users import User
# from app.dao.model.movies import Movie
# from app.dao.model.favorites import FavoriteMovie

from app.dao.model.base import Base  # noqa

os.environ['TESTING'] = 'TRUE'

from app.setup_db import engine  # noqa

# engine = create_engine('sqlite:///:memory:', echo=True)


@pytest.fixture(scope='session')
def db_migration():
    with engine.begin() as conn:
        Base.metadata.drop_all(conn)
        Base.metadata.create_all(conn)


@pytest.fixture()
def db_session(db_migration):
    with sessionmaker(autocommit=False, autoflush=False, bind=engine)() as db_session:
        yield db_session
        db_session.rollback()
