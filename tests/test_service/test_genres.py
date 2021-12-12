from unittest.mock import Mock, patch

import pytest

from app.dao.model.genres import Genre, GenreBM
from app.errors import NotFoundError
from app.service.genres import GenreService

genres_ld = [
    {
        'id': 1,
        'name': 'Комедия'
    },
    {
        'id': 2,
        'name': 'Мюзикл'
    },
    {
        'id': 3,
        'name': 'Вестерн'
    },
]


class TestGenreService:

    @pytest.fixture
    def genre(self, db_session):
        obj = Genre(id=1, name='Комедия')
        db_session.add(obj)
        db_session.flush()
        return obj

    @pytest.fixture
    def dao(self):
        with patch('app.service.genres.GenreDAO') as mock:
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

    def test_get_one(self, db_session, genre):
        assert GenreService(db_session).get_one(genre.id) == {'id': genre.id, 'name': genre.name}

    def test_get_one_with_mock(self, db_session, dao):
        genre = Genre(id=1, name='Комедия')
        dao().get_one.return_value = GenreBM.from_orm(genre).dict()

        assert GenreService(db_session).get_one(genre.id) == {'id': genre.id, 'name': genre.name}
        dao().get_one.assert_called_once_with(1)

    def test_get_one_not_found(self, db_session):
        with pytest.raises(NotFoundError):
            GenreService(db_session).get_one(1)

    def test_all_with_mock(self, db_session, dao):
        temp = []
        for item in genres_ld:
            temp.append(GenreBM.from_orm(Genre(**item)).dict())
        dao().get_all.return_value = temp

        assert GenreService(db_session).get_all() == genres_ld

    def test_create_with_mock(self, db_session, dao):
        genre = Genre(id=4, name='Триллер')
        dao().create.return_value = GenreBM.from_orm(genre).dict()

        assert GenreService(db_session).create({'id': genre.id, 'name': genre.name})\
               == {'id': genre.id, 'name': genre.name}

    def test_update_with_mock(self, db_session, dao):
        genre = Genre(id=4, name='Триллер')
        dao().update.return_value = GenreBM.from_orm(genre).dict()

        assert GenreService(db_session).update({'id': genre.id, 'name': genre.name}, 4)\
               == {'id': genre.id, 'name': genre.name}

    def test_delete_with_mock(self, db_session, dao):
        dao().delete.return_value = None

        assert GenreService(db_session).delete(1) is None

    def test_all_by_filter_with_mock(self, db_session, dao):
        dao().get_all_by_filter.return_value = [{'id': 1, 'name': 'Триллер'}]

        assert GenreService(db_session).get_all_by_filter({'id': 1}) == [{'id': 1, 'name': 'Триллер'}]

    def test_part_update_with_mock(self, db_session, dao):
        assert GenreService(db_session).part_update() is None
