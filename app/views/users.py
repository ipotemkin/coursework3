from fastapi import APIRouter, status, Response, Depends
from app.dao.model.users import UserBM, UserUpdateBM
from app.service.users import UserService
from app.dependencies import get_db, valid_token, valid_admin_token
from sqlalchemy.orm import Session

router = APIRouter(prefix='/users', tags=['users'], dependencies=[Depends(valid_token)])


@router.get('', summary='Получить всех пользователей')
async def users_get_all(db: Session = Depends(get_db)):
    """
    Получить всех пользователей
    """
    res = UserService(session=db).get_all()
    return res


@router.get('/{pk}', summary='Получить пользователя по его ID')
async def users_get_one(pk: int, db: Session = Depends(get_db)):
    """
    Получить пользователя по ID:

    - **pk**: ID пользователя
    """
    return UserService(db).get_one(pk)


@router.post('', status_code=status.HTTP_201_CREATED, summary='Добавить пользователя',
             response_description="The created item")
async def users_post(user: UserBM, response: Response, db: Session = Depends(get_db)):
    """
    Добавить пользователя:

    - **id**: ID пользователя - целое число (необязательный параметр)
    - **name**: имя пользователя (обязательный параметр)
    - **role**: роль пользователя
    - **password**: пароль пользователя
    """
    new_obj = UserService(db).create(user.dict())
    response.headers['Location'] = f'{router.prefix}/{new_obj.id}'
    return []


@router.patch('/{pk}',
              # status_code=status.HTTP_204_NO_CONTENT,
              summary='Изменить запись пользователя с указанным ID',
              dependencies=[Depends(valid_admin_token)])
async def users_update(user: UserUpdateBM, pk: int, db: Session = Depends(get_db)):
    """
    Изменить запись пользователя с указанным ID:

    - **name**: изменить имя пользователя
    - **role**: изменить роль пользователя
    - **password**: изменить пароль пользователя
    """
    return UserService(db).update(user.dict(), pk)


@router.delete('/{pk}', status_code=status.HTTP_200_OK, summary='Удалить запись пользователя с указанным ID')
async def users_delete(pk: int, db: Session = Depends(get_db)):
    """
    Удалить запись пользователя с указанным ID:
    """
    UserService(db).delete(pk)
