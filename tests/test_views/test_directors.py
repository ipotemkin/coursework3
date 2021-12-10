import os
from http import HTTPStatus
import pytest
from app.dao.model.directors import Director
from fixtures import data
from run import app
from fastapi.testclient import TestClient


os.environ['TESTING'] = 'True'

client = TestClient(app)


# def test_health_check():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"Hello": "World"}

# @pytest.fixture
# def application():
#     # app = create_app("testing")
#     # with app.app_context():
#     #     yield app
#     return app
#
#
# @pytest.fixture
# def client(application, db_session):
#     # with application.test_client() as client:
#
#     # with app as client:
#     #     yield client
#     return client

# @pytest.fixture()
# def client():
#     return app

class TestDirectorsView:
    # @pytest.fixture
    # def director(self, db_session):
    #     obj = Director(id=1, name='Spillberg')
    #     db_session.add(obj)
    #     db_session.flush()
    #     return obj

    def test_many(self):
        response = client.get("/directors/")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == data['directors']

    def test_many_with_page(self):
        response = client.get("/directors/?page=1")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == data['directors'][:2]

    def test_one(self):
        response = client.get("/directors/1")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == data['directors'][0]

    def test_one_not_found(self):
        response = client.get("/directors/1000")
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'message': 'Not Found'}



    # def test_director_pages(self, client, director):
    #     response = client.get("/directors/?page=1")
    #     assert response.status_code == HTTPStatus.OK
    #     assert len(response.json) == 1
    #
    #     response = client.get("/directors/?page=2")
    #     assert response.status_code == HTTPStatus.OK
    #     assert len(response.json) == 0
    #
    # def test_director(self, client, director):
    #     response = client.get("/directors/1")
    #     assert response.status_code == HTTPStatus.OK
    #     assert response.json == {"id": director.id, "name": director.name}
    #
    # def test_director_not_found(self, client, director):
    #     response = client.get("/directors/2")
    #     assert response.status_code == HTTPStatus.NOT_FOUND
