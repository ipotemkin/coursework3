from fastapi import APIRouter, status, Response, Depends
from app.dao.model.directors import DirectorBM, DirectorUpdateBM
from app.service.directors import DirectorService
from app.dependencies import get_db
from sqlalchemy.orm import Session
import time

router = APIRouter(prefix='/directors', tags=['directors'])


@router.get('', summary='Получить всех режиссеров')
async def directors_get_all(db: Session = Depends(get_db)):
    """
    Получить всех режиссеров
    """
    # t0 = time.perf_counter()
    # res = director_service.get_all()
    res = DirectorService(session=db).get_all()
    # elapsed = time.perf_counter() - t0
    # print('with sqlalchemy [%0.8fs]' % elapsed)
    return res


@router.get('/{pk}', summary='Получить режиссера по его ID')
async def directors_get_one(pk: int, db: Session = Depends(get_db)):
    """
    Получить режиссера по ID:

    - **pk**: ID режиссера
    """
    return DirectorService(db).get_one(pk)
    # return director_service.get_one(pk)


@router.post('', status_code=status.HTTP_201_CREATED, summary='Добавить режиссера',
             response_description="The created item")
async def directors_post(director: DirectorBM, response: Response, db: Session = Depends(get_db)):
    """
    Добавить режиссера:

    - **id**: ID режиссера - целое число (необязательный параметр)
    - **name**: имя режиссера (обязательный параметр)
    """
    new_obj = DirectorService(db).create(director.dict())
    # new_obj = director_service.create(director.dict())
    response.headers['Location'] = f'{router.prefix}/{new_obj.id}'
    return []


@router.patch('/{pk}',
              # status_code=status.HTTP_204_NO_CONTENT,
              summary='Изменить запись режиссера с указанным ID')
async def directors_update(director: DirectorUpdateBM, pk: int, db: Session = Depends(get_db)):
    """
    Изменить запись режиссера с указанным ID:

    - **name**: изменить имя режиссера
    """
    return DirectorService(db).update(director.dict(), pk)
    # return director_service.update(director.dict(), pk)


@router.delete('/{pk}', status_code=status.HTTP_200_OK, summary='Удалить запись режиссера с указанным ID')
async def directors_delete(pk: int, db: Session = Depends(get_db)):
    """
    Удалить запись режиссера с указанным ID:
    """
    DirectorService(db).delete(pk)
    # director_service.delete(pk)
    # return None
