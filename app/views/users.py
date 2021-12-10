from fastapi import APIRouter, status, Response, Depends
from app.dao.model.users import UserBM, UserUpdateBM
from app.service.users import UserService
from app.dependencies import get_db, valid_token
from sqlalchemy.orm import Session
from pydantic import BaseModel

router = APIRouter(prefix='/user', tags=['users'])


class PasswordChange(BaseModel):
    password_1: str
    password_2: str

    class Config:
        orm_mode = True


@router.get('', summary='Получить текущего пользователя')
@router.get('/', include_in_schema=False)
async def users_current_user(db: Session = Depends(get_db), decoded_token=Depends(valid_token)):
    """
    Получить текущего пользователя
    """
    pk = UserService(db).get_all_by_filter({'email': decoded_token.get('email')})[0].get('id')
    res = UserService(session=db).get_one(pk)
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
    return new_obj


@router.patch('',
              # status_code=status.HTTP_204_NO_CONTENT,
              summary='Изменить запись текущего пользователя',
              )
@router.patch('/',
              # status_code=status.HTTP_204_NO_CONTENT,
              include_in_schema=False
              )
async def current_user_update(user: UserUpdateBM,
                              db: Session = Depends(get_db),
                              decoded_token=Depends(valid_token)
                              ):
    """
    Изменить запись текущего пользователя:

    - **name**: изменить имя пользователя
    - **role**: изменить роль пользователя
    - **password**: изменить пароль пользователя
    """
    pk = UserService(db).get_all_by_filter({'email': decoded_token.get('email')})[0].get('id')
    return UserService(db).update(user.dict(), pk)


@router.put('/password',
            # status_code=status.HTTP_204_NO_CONTENT,
            summary='Обновить пароль пользователя с указанным ID',
            )
async def users_update_password(body: PasswordChange, db: Session = Depends(get_db),
                                decoded_token=Depends(valid_token)):
    """
    Обновить пароль пользователя с указанным ID:

    - **password_1**: старый пароль пользователя
    - **password_2**: новый пароль пользователя
    """
    pk = UserService(db).get_all_by_filter({'email': decoded_token.get('email')})[0].get('id')
    return UserService(db).update_password(pk, body.password_1, body.password_2)
