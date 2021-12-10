from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from os import environ

# use these 2 lines to give the db metadata to alembic
from app.dao.model import directors, genres, movies, users, rtokens, favorites  # noqa F401
from app.dao.model.base import Base  # noqa


BASE_DIR = Path(__file__).parent

TESTING = environ.get("TESTING")  # this will be used by pytest

if TESTING:
    engine = create_engine(
        f"sqlite:///{BASE_DIR.parent}/movies_test.db",
        connect_args={'check_same_thread': False},
        echo=True)

else:
    engine = create_engine(
        f"sqlite:///{BASE_DIR.parent}/movies.db",
        connect_args={'check_same_thread': False},
        echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
