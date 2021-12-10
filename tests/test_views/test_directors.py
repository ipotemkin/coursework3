import os
from http import HTTPStatus
import pytest
from app.dao.model.directors import Director, DirectorBM
from fixtures import data
from run import app
from fastapi.testclient import TestClient

client = TestClient(app)

test_director = {"id": 100, "name": "Никита Михалков"}


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
    @pytest.fixture
    def directors(self, db_session):
        for i in data['directors']:
            db_session.add(Director(**i))
            db_session.commit()
        return data['directors']

    @pytest.fixture
    def new_director(self, db_session):
        obj = Director(id=100, name='Михалков')
        db_session.add(obj)
        db_session.commit()
        return obj

    def test_testing_is_true(self):
        assert os.environ.get("TESTING") == 'TRUE'

    def test_many(self, db_session, directors):
        response = client.get("/directors/")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == directors

    def test_many_with_page(self):
        response = client.get("/directors/?page=1")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == data['directors'][:2]

    def test_one(self, db_session):
        response = client.get("/directors/1")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == data['directors'][0]

    def test_one_not_found(self, db_session):
        response = client.get("/directors/1000")
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'message': 'Not Found'}

    def test_update(self, new_director, db_session):
        response = client.patch("/directors/100", json=test_director)
        assert response.status_code == HTTPStatus.OK
        assert response.json() == test_director

    def test_create(self, db_session):
        new_director = {"id": 101, "name": "Никита Михалков"}
        response = client.post("/directors", json=new_director)
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {"id": 101, "name": "Никита Михалков"}

    def test_delete(self, db_session):
        response = client.delete("/directors/100")
        assert response.status_code == HTTPStatus.OK
        response = client.get("/directors/100")
        assert response.status_code == HTTPStatus.NOT_FOUND
