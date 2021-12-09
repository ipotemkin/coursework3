from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

BASE_DIR = Path(__file__).parent

engine = create_engine(f"sqlite:///{BASE_DIR.parent}/movies.db",
                       connect_args={'check_same_thread': False},
                       echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def init_db():
#     # Base.metadata.create_all(bind=engine)
#     print(Base.metadata.__dict__)  # TODO: remove on release
