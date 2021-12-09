from app.service.basic import BasicService
from app.dao.favorites import FavoriteMovieDAO
from app.service.movies import MovieService
from app.dao.model.movies import MovieBMSimple
from app.constants import ITEMS_ON_PAGE
from app.errors import NotFoundError


class FavoriteMovieService(BasicService):
    def __init__(self, session):
        super().__init__(FavoriteMovieDAO(session))

    def get_all_by_user(self, user_id, page=None):
        sql = f"""
        select m.id as id,
            description,
            rating,
            title,
            director_id,
            genre_id,
            year,
            trailer
        from movie as m
            join favorite_movie as f on m.id = f.movie_id
        where f.user_id = {user_id}
        """
        if page is not None:
            start_at = (page - 1) * ITEMS_ON_PAGE
            sql += f' limit {ITEMS_ON_PAGE} offset {start_at}'
        if not (res := self.dao.session.execute(sql).all()):
            raise NotFoundError
        return [MovieBMSimple.from_orm(obj).dict() for obj in res]
