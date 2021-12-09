from unittest.mock import Mock, patch

import pytest

from app.dao.model.favotites import FavoriteMovie, FavoriteMovieBM
from app.dao.model.movies import Movie, MovieBMSimple
from app.service.favorites import FavoriteMovieService

from app.errors import NotFoundError

fav_movies_ld = [
    {
        'id': 1,
        'user_id': 1,
        'movie_id': 1
    },
    {
        'id': 2,
        'user_id': 1,
        'movie_id': 2
    },
    {
        'id': 3,
        'user_id': 2,
        'movie_id': 1
    },
]

movie = Movie(
    id=1,
    description="qwerty",
    rating=5.0,
    title="Test",
    director_id=1,
    genre_id=1,
    year=2020,
    trailer="#"
)


class TestFavoriteMovieService:
    @pytest.fixture
    def favorite_movie(self, db_session):
        # obj = FavoriteMovie(id=1, user_id=1, movie_id=1)
        # obj
        for i in fav_movies_ld:
            db_session.add(FavoriteMovie(**i))

        db_session.add(movie)
        db_session.flush()
        # return obj

    @pytest.fixture
    def dao(self):
        with patch('app.service.favorites.FavoriteMovieDAO') as mock:
            mock.return_value = Mock(
                get_one=Mock(),
                get_all=Mock(),
                create=Mock(),
                update=Mock(),
                delete=Mock(),
                get_all_by_filter=Mock(),
                part_update=Mock()
            )
            yield mock

    # def test_get_one(self, db_session, favorite_movie):
    #     assert FavoriteMovieService(db_session).get_one(favorite_movie.id) \
    #            == {'id': favorite_movie.id, 'user_id': favorite_movie.user_id, 'movie_id': favorite_movie.movie_id}

    def test_get_one_with_mock(self, db_session, dao):
        # pass
        favorite_movie = FavoriteMovie(id=1, user_id=1, movie_id=1)
        dao().get_one.return_value = FavoriteMovieBM.from_orm(favorite_movie).dict()

        assert FavoriteMovieService(db_session).get_one(favorite_movie.id) \
               == {'id': 1, 'user_id': 1, 'movie_id': 1}
        dao().get_one.assert_called_once_with(1)

    def test_get_one_not_found(self, db_session):
        with pytest.raises(NotFoundError):
            FavoriteMovieService(db_session).get_one(1)

    def test_all_with_mock(self, db_session, dao):
        temp = []
        for item in fav_movies_ld:
            temp.append(FavoriteMovieBM.from_orm(FavoriteMovie(**item)).dict())
        dao().get_all.return_value = temp

        assert FavoriteMovieService(db_session).get_all() == fav_movies_ld

    def test_get_all_not_found(self, db_session):
        with pytest.raises(NotFoundError):
            assert FavoriteMovieService(db_session).get_all() == []

    def test_create_with_mock(self, db_session, dao):
        favorite_movie = FavoriteMovie(id=4, user_id=3, movie_id=5)
        dao().create.return_value = FavoriteMovieBM.from_orm(favorite_movie).dict()

        assert FavoriteMovieService(db_session).create(
            {'id': favorite_movie.id, 'user_id': favorite_movie.user_id, 'movie_id': favorite_movie.movie_id}) == {
            'id': favorite_movie.id, 'user_id': favorite_movie.user_id, 'movie_id': favorite_movie.movie_id}

    def test_update_with_mock(self, db_session, dao):
        favorite_movie = FavoriteMovie(id=4, user_id=3, movie_id=5)
        dao().update.return_value = FavoriteMovieBM.from_orm(favorite_movie).dict()

        assert FavoriteMovieService(db_session).update(
            {'id': favorite_movie.id, 'user_id': favorite_movie.user_id, 'movie_id': favorite_movie.movie_id}, 4) == {
            'id': favorite_movie.id, 'user_id': favorite_movie.user_id, 'movie_id': favorite_movie.movie_id}

    def test_delete_with_mock(self, db_session, dao):
        dao().delete.return_value = None

        assert FavoriteMovieService(db_session).delete(1) is None

    def test_all_by_filter_with_mock(self, db_session, dao):
        # temp = []
        # for item in directors_ld:
        #     temp.append(DirectorBM.from_orm(Director(**item)).dict())
        dao().get_all_by_filter.return_value = [{'id': 1, 'user_id': 1, 'movie_id': 1}]

        assert FavoriteMovieService(db_session).get_all_by_filter({'id': 1}) == [{'id': 1, 'user_id': 1, 'movie_id': 1}]

    def test_part_update_with_mock(self, db_session, dao):
        assert FavoriteMovieService(db_session).part_update() is None

    def test_get_all_by_user(self, db_session, favorite_movie):
        assert FavoriteMovieService(db_session).get_all_by_user(user_id=2) == [
            MovieBMSimple.from_orm(movie).dict()]

    def test_get_all_by_user_with_page(self, db_session, favorite_movie):
        assert FavoriteMovieService(db_session).get_all_by_user(user_id=2, page=1) == [
            MovieBMSimple.from_orm(movie).dict()]

    # def test_get_all_not_found(self, db_session):
    #     with pytest.raises(NotFoundError):
    #         assert FavoriteMovieService(db_session).get_all() == []
