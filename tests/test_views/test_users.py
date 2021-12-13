import os
from http import HTTPStatus
import pytest
from app.dao.model.users import User
from fixtures import data
from run import app
from fastapi.testclient import TestClient
from app.constants import ITEMS_ON_PAGE
from app.service.users import UserService
from tests.test_views.conftest import db_session


client = TestClient(app)

test_user_request = {
    "email": "test3@example.com",
    "password": "test3",
    "role": "user",
    "name": "Sarah",
    "surname": "Fern",
    "favorite_genre": 17,
}

test_user_response = {
    "email": "test3@example.com",
    "password": UserService(db_session).get_hash("test3"),
    "role": "user",
    "name": "Sarah",
    "surname": "Fern",
    "favorite_genre": 17,
}

test_users = [
    {
        "email": "test@example.com",
        "password": "test",
        "role": "user",
        "name": "James",
        "surname": "Fern",
        "favorite_genre": 17,
    },
    {
        "email": "test2@example.com",
        "password": "test2",
        "role": "user",
        "name": "Mary",
        "surname": "Smith",
        "favorite_genre": 4,
    },
]

test_users_response = [
    {
        "email": "test@example.com",
        "password": UserService(db_session).get_hash("test"),
        "role": "user",
        "name": "James",
        "surname": "Fern",
        "favorite_genre": 17,
        "id": 1,
    },
    {
        "email": "test2@example.com",
        "password": UserService(db_session).get_hash("test2"),
        "role": "user",
        "name": "Mary",
        "surname": "Smith",
        "favorite_genre": 4,
        "id": 2,
    },
]

ACCESS_TOKEN = ""


class TestMoviesView:
    @pytest.fixture
    def users(self, db_session):
        for i in test_users:
            # db_session.add(User(**i))
            # db_session.commit()
            UserService(db_session).create(i)
        return test_users

    @pytest.fixture
    def token(self, db_session):
        request_data = {
            "email": "test@example.com",
            "password": "test",
        }

        response = client.post(
            "/auth/login",
            json=request_data,
        )
        global ACCESS_TOKEN
        ACCESS_TOKEN = response.json()['access_token']
        return ACCESS_TOKEN

    # @pytest.fixture
    # def new_user(self, db_session):
    #     obj = User(**test_user_request)
    #     db_session.add(obj)
    #     db_session.commit()
    #     return obj

    def test_testing_is_true(self):
        assert os.environ.get("TESTING") == 'TRUE'

    def test_get_current_user_info(self, db_session, users, token):
        response = client.get(
            "/user",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == test_users_response[0]

    def test_update_current_user(self, db_session):
        response = client.patch(
            "/user",
            json={"name": "Bob"},
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
        test_users_response[0]["name"] = "Bob"
        assert response.status_code == HTTPStatus.OK
        assert response.json() == test_users_response[0]

    def test_update_user_password(self, db_session):
        response = client.put(
            "/user/password",
            json={"password_1": "test", "password_2": "test2"},
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() is None

    # def test_many_with_page(self):
    #     response = client.get("/users/?page=1")
    #     assert response.status_code == HTTPStatus.OK
    #     assert response.json() == test_users_response[:ITEMS_ON_PAGE]
    #
    # def test_many_with_director_id(self):
    #     response = client.get("/users/?director_id=1")
    #     assert response.status_code == HTTPStatus.OK
    #     assert response.json() == test_users_response[0:1]
    #
    # def test_many_with_genre_id(self):
    #     response = client.get("/users/?genre_id=6")
    #     assert response.status_code == HTTPStatus.OK
    #     assert response.json() == test_users_response[14:15]
    #
    # def test_many_with_year(self):
    #     response = client.get("/users/?year=1978")
    #     assert response.status_code == HTTPStatus.OK
    #     assert response.json() == test_users_response[2:3]
    #
    # def test_many_with_year_not_found(self):
    #     response = client.get("/users/?year=2030")
    #     assert response.status_code == HTTPStatus.OK
    #     assert response.json() == []
    #
    # def test_many_with_director_id_genre_id_year(self):
    #     response = client.get("/users/?director_id=2&genre_id=17&year=2012")
    #     assert response.status_code == HTTPStatus.OK
    #     assert response.json() == test_users_response[3:4]
    #
    # def test_many_with_director_id_genre_id_year_not_found(self):
    #     response = client.get("/users/?director_id=2&genre_id=17&year=2030")
    #     assert response.status_code == HTTPStatus.OK
    #     assert response.json() == []
    #
    # def test_one(self, db_session):
    #     response = client.get("/users/1")
    #     assert response.status_code == HTTPStatus.OK
    #     assert response.json() == test_users_response[0]
    #
    # def test_one_not_found(self, db_session):
    #     response = client.get("/users/1000")
    #     assert response.status_code == HTTPStatus.NOT_FOUND
    #     assert response.json() == {'message': 'Not Found'}
