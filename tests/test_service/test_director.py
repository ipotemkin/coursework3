from unittest.mock import MagicMock, patch
import pytest
import pydantic

from app.dao.model.directors import Director
from app.dao.directors import DirectorDAO
from app.service.directors import DirectorService
# from app.setup_db import db
from app.dependencies import get_db


# @pytest.fixture()
# def some_func():
#     return DirectorService(get_db()).get_one(1)


def test_director_service_get_one():
    with patch('app.service.directors.DirectorDAO') as mock:
        instance = mock.return_value
        instance.get_one.return_value = Director(id=1, name='Spillberg')
        assert DirectorService(get_db()).get_one(1) == Director(id=1, name='Spillberg')



# @pytest.fixture()
# def DirectorDAO():
#     DirectorDAO = MagicMock()
#
#     spillberg = Director(id=1, name='Spillberg')
#     tarantino = Director(id=2, name='Tarantino')
#     cameron = Director(id=3, name='Cameron')
#
#     objects_d = {1: spillberg, 2: tarantino, 3: cameron}
#     director_dao.get_one = MagicMock(side_effect=objects_d.get)
#     director_dao.get_all = MagicMock(return_value=[spillberg, tarantino, cameron])
#     director_dao.create = MagicMock(return_value=Director(id=3))
#     director_dao.delete = MagicMock()
#     director_dao.update = MagicMock()
#     director_dao.partially_update = MagicMock()
#
#     return DirectorDAO
#
#
# class TestDirectorService:
#     @pytest.fixture(autouse=True)
#     def director_service(self, director_dao):
#         self.director_service = DirectorService(dao=director_dao)
#
#     def test_get_one(self):
#         director = self.director_service.get_one(1)
#         assert director is not None
#         assert director.id is not None
#         assert director.name == 'Spillberg'
#
#     def test_get_one_100(self):
#         director = self.director_service.get_one(100)
#         assert director is None
#
#     def test_get_all(self):
#         directors = self.director_service.get_all()
#         assert len(directors) > 0
#         assert isinstance(directors, list)
#
#     def test_create(self):
#         director_d = {
#             'name': 'Kubrik'
#         }
#         director = self.director_service.create(director_d)
#         assert director.id is not None
#
#     def test_create_fail(self):
#         director_d = {
#             'id': 1,
#             'name': 'Kubrik'
#         }
#         director = self.director_service.create(director_d)
#         assert director.id is not None
#
#     def test_delete(self):
#         assert self.director_service.delete(1) is None
#
#     def test_update(self):
#         director_d = {
#             'id': 3,
#             'name': 'Kubrik'
#         }
#         assert self.director_service.update(director_d) is not None
#
#     def test_partially_update(self):
#         director_d = {
#             'id': 3,
#             'name': 'Kubrik'
#         }
#         self.director_service.partially_update(director_d)
