import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.dao.model.users import User
from app.dao.model.movies import Movie
from app.dao.model.favotites import FavoriteMovie
from app.dao.model.base import Base

engine = create_engine('sqlite:///:memory:', echo=True)


@pytest.fixture(scope='module')
def db_migration():
    with engine.begin() as conn:
        Base.metadata.drop_all(conn)
        Base.metadata.create_all(conn)


@pytest.fixture
def db_session(db_migration):
    with sessionmaker(autocommit=False, autoflush=False, bind=engine)() as db_session:
        yield db_session
        db_session.rollback()
