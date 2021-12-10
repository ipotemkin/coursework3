from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from os import environ


from app.dao.model.directors import Director
from app.dao.model.users import User
from app.dao.model.movies import Movie
from app.dao.model.favotites import FavoriteMovie

from app.dao.model.base import Base  # noqa


BASE_DIR = Path(__file__).parent

TESTING = environ.get("TESTING")

# engine = create_engine(
#     f"sqlite:///:memory:",
#     connect_args={'check_same_thread': False},
#     echo=True)

# engine = create_engine(
#     f"sqlite:///{BASE_DIR.parent}/movies.db",
#     connect_args={'check_same_thread': False},
#     echo=True)


if TESTING:
    eng = create_engine(
        f"sqlite:///{BASE_DIR.parent}/movies_test.db",
        # f"sqlite:///:memory:",
        connect_args={'check_same_thread': False},
        echo=True)
    # with eng.begin() as conn:
    #     Base.metadata.drop_all(conn)
    #     # breakpoint()
    #     Base.metadata.create_all(conn)

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
