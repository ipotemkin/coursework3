from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, ForeignKey
from app.dao.model.base import Base


class FavoriteMovie(Base):
    __tablename__ = 'favorite_movie'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movie.id'), nullable=False)

    def __repr__(self):
        return f"<Favorite: id={self.id}, user_id={self.user_id}, movie_id={self.movie_id}>"


class FavoriteMovieBase(BaseModel):
    user_id: int
    movie_id: int

    class Config:
        orm_mode = True


class FavoriteMovieBM(FavoriteMovieBase):
    id: Optional[int]


class FavoriteMovieUpdateBM(FavoriteMovieBase):
    user_id: Optional[int]
    movie_id: Optional[int]
