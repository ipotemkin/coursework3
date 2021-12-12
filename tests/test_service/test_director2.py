from unittest.mock import Mock, patch

import pytest

from app.dao.model.directors import Director, DirectorBM
from app.errors import NotFoundError
from app.service.directors import DirectorService

directors_ld = [
    {
        'id': 1,
        'name': 'Spillberg'
    },
    {
        'id': 2,
        'name': 'Tarantino'
    },
    {
        'id': 3,
        'name': 'Kubrik'
    },
]


class TestDirectorService:
    @pytest.fixture
    def director(self, db_session):
        obj = Director(id=1, name='Spillberg')
        db_session.add(obj)
        db_session.flush()
        return obj

    @pytest.fixture
    def dao(self):
        with patch('app.service.directors.DirectorDAO') as mock:
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

    def test_get_one(self, db_session, director):
        assert DirectorService(db_session).get_one(director.id) == {'id': director.id, 'name': director.name}

    def test_get_one_with_mock(self, db_session, dao):
        director = Director(id=1, name='Spillberg')
        dao().get_one.return_value = DirectorBM.from_orm(director).dict()

        assert DirectorService(db_session).get_one(director.id) == {'id': director.id, 'name': director.name}
        dao().get_one.assert_called_once_with(1)

    def test_get_one_not_found(self, db_session):
        with pytest.raises(NotFoundError):
            DirectorService(db_session).get_one(1)

    def test_all_with_mock(self, db_session, dao):
        temp = []
        for item in directors_ld:
            temp.append(DirectorBM.from_orm(Director(**item)).dict())
        dao().get_all.return_value = temp

        assert DirectorService(db_session).get_all() == directors_ld

    def test_create_with_mock(self, db_session, dao):
        director = Director(id=4, name='Spillberg')
        dao().create.return_value = DirectorBM.from_orm(director).dict()

        assert DirectorService(db_session).create({'id': director.id, 'name': director.name})\
               == {'id': director.id, 'name': director.name}

    def test_update_with_mock(self, db_session, dao):
        director = Director(id=4, name='Spillberg')
        dao().update.return_value = DirectorBM.from_orm(director).dict()

        assert DirectorService(db_session).update({'id': director.id, 'name': director.name}, 4)\
               == {'id': director.id, 'name': director.name}

    def test_delete_with_mock(self, db_session, dao):
        dao().delete.return_value = None

        assert DirectorService(db_session).delete(1) is None

    def test_all_by_filter_with_mock(self, db_session, dao):
        dao().get_all_by_filter.return_value = [{'id': 1, 'name': 'Spillberg'}]

        assert DirectorService(db_session).get_all_by_filter({'id': 1}) == [{'id': 1, 'name': 'Spillberg'}]

    def test_part_update_with_mock(self, db_session, dao):
        assert DirectorService(db_session).part_update() is None
