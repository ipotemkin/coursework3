from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from os import environ

# TODO: нужно разобраться с необходимостью этого блока. У алембика были проблемы с созданием таблиц без этих строк
# ------------------------------------------------
# Option 1
# from app.dao.model import directors, genres, movies, users, rtokens, favorites

# Option 2
# from app.dao.model.directors import Director
# from app.dao.model.users import User
# from app.dao.model.movies import Movie
# from app.dao.model.favorites import FavoriteMovie
# ---------------------------------------------------

from app.dao.model.base import Base  # noqa


BASE_DIR = Path(__file__).parent

TESTING = environ.get("TESTING")


if TESTING:
    eng = create_engine(
        f"sqlite:///{BASE_DIR.parent}/movies_test.db",
        # f"sqlite:///:memory:",
        connect_args={'check_same_thread': False},
        echo=True)

else:
    eng = create_engine(
        f"sqlite:///{BASE_DIR.parent}/movies.db",
        connect_args={'check_same_thread': False},
        echo=True)

engine = eng

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def init_db():
#     # Base.metadata.create_all(bind=engine)
#     print(Base.metadata.__dict__)  # TODO: remove on release
