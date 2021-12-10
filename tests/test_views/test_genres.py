import os
from http import HTTPStatus
import pytest
from app.dao.model.genres import Genre
from fixtures import data
from run import app
from fastapi.testclient import TestClient
from app.constants import ITEMS_ON_PAGE

client = TestClient(app)

test_genre = {"id": 100, "name": "Новое кино"}


class TestGenresView:
    @pytest.fixture
    def genres(self, db_session):
        for i in data['genres']:
            db_session.add(Genre(**i))
            db_session.commit()
        return data['genres']

    @pytest.fixture
    def new_genre(self, db_session):
        obj = Genre(**test_genre)
        db_session.add(obj)
        db_session.commit()
        return obj

    def test_testing_is_true(self):
        assert os.environ.get("TESTING") == 'TRUE'

    def test_many(self, db_session, genres):
        response = client.get("/genres/")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == genres

    def test_many_with_page(self):
        response = client.get("/genres/?page=1")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == data['genres'][:ITEMS_ON_PAGE]

    def test_one(self, db_session):
        response = client.get("/genres/1")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == data['genres'][0]

    def test_one_not_found(self, db_session):
        response = client.get("/genres/1000")
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'message': 'Not Found'}

    def test_update(self, new_genre, db_session):
        response = client.patch("/genres/100", json=test_genre)
        assert response.status_code == HTTPStatus.OK
        assert response.json() == test_genre

    def test_create(self, db_session):
        new_genre = {"id": 101, "name": "Новый жанр"}
        response = client.post("/genres", json=new_genre)
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {"id": 101, "name": "Новый жанр"}

    def test_delete(self, db_session):
        response = client.delete("/genres/100")
        assert response.status_code == HTTPStatus.OK
        response = client.get("/genres/100")
        assert response.status_code == HTTPStatus.NOT_FOUND
