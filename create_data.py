from sqlalchemy.orm import Session
from app.setup_db import engine
from app.dao.model import directors, genres, movies, users, rtokens, favorites
from app.dao.model.base import Base
from fixtures import data
from app.dao.model.directors import Director
from app.dao.model.genres import Genre
from app.dao.model.movies import Movie

print("tables:")
for i in Base.metadata.__dict__['tables']:
    print(i)

db = Session(bind=engine)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

for director in data['directors']:
    db.add(Director(**director))

for genre in data['genres']:
    db.add(Genre(**genre))

for movie in data['movies']:
    db.add(Movie(**movie))

db.commit()
