from unittest.mock import Mock, patch

import pytest

from app.dao.model.users import User, UserBM
from app.errors import NotFoundError
from app.service.users import UserService

users_ld = [
    {
        'id': 1,
        'email': 'test@example.com',
        'name': 'test',
        'surname': 'Fern',
        'password': '\x1aCf6,\x1e<.\n|M$%;_\nH`',
        'favorite_genre': 1,
        'role': 'user'
    },
    {
        'id': 2,
        'email': 'test2@example.com',
        'name': 'test2',
        'surname': 'Smith',
        'password': 'test2',
        'favorite_genre': 17,
        'role': 'user'
    },
]


class TestUserService:
    @pytest.fixture
    def user(self, db_session):
        obj = User(**users_ld[0])
        db_session.add(obj)
        db_session.flush()
        return obj

    @pytest.fixture
    def dao(self):
        with patch('app.service.users.UserDAO') as mock:
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

    def test_get_one(self, db_session, user):
        assert UserService(db_session).get_one(user.id) == UserBM.from_orm(user).dict()

    def test_get_one_with_mock(self, db_session, dao):
        user = User(**users_ld[0])
        dao().get_one.return_value = UserBM.from_orm(user).dict()

        assert UserService(db_session).get_one(user.id) == UserBM.from_orm(user).dict()
        dao().get_one.assert_called_once_with(1)

    def test_get_one_not_found(self, db_session):
        with pytest.raises(NotFoundError):
            UserService(db_session).get_one(1)

    def test_all_with_mock(self, db_session, dao):
        temp = []
        for item in users_ld:
            temp.append(UserBM.from_orm(User(**item)).dict())
        dao().get_all.return_value = temp

        assert UserService(db_session).get_all() == users_ld

    def test_create_with_mock(self, db_session, dao):
        new_user = users_ld[0]
        new_user['id'] = 3
        new_user['email'] = 'test3@example.com'
        user = User(**new_user)
        dao().create.return_value = UserBM.from_orm(user).dict()
        new_user['password'] = 'test'
        res = UserService(db_session).create(new_user)
        new_user['password'] = '\x1aCf6,\x1e<.\n|M$%;_\nH`'

        assert res == new_user

    def test_update_with_mock(self, db_session, dao):
        update_user = users_ld[1]
        update_user['password'] = None
        user = User(**update_user)
        dao().update.return_value = UserBM.from_orm(user).dict()

        assert UserService(db_session).update(UserBM.from_orm(user).dict(), 2) == users_ld[1]

    def test_delete_with_mock(self, db_session, dao):
        dao().delete.return_value = None

        assert UserService(db_session).delete(1) is None

    def test_all_by_filter_with_mock(self, db_session, dao):
        dao().get_all_by_filter.return_value = [users_ld[0]]

        assert UserService(db_session).get_all_by_filter({'id': 1}) == [users_ld[0]]

    def test_part_update_with_mock(self, db_session, dao):
        assert UserService(db_session).part_update() is None
