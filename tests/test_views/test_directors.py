from http import HTTPStatus
import pytest
from app.dao.model.directors import Director

from run import app


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

@pytest.fixture()
def client():
    return app


class TestDirectorsView:
    @pytest.fixture
    def director(self, db_session):
        obj = Director(id=1, name='Spillberg')
        db_session.add(obj)
        db_session.flush()
        return obj

    def test_many(self, client, director):
        response = client.get("/directors/")
        assert response.status_code == HTTPStatus.OK
        assert response.json == [{"id": director.id, "name": director.name}]

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
