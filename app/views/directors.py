from fastapi import APIRouter, Depends
from app.service.directors import DirectorService
from app.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix='/directors', tags=['directors'])


@router.get('', summary='Получить всех режиссеров')
@router.get('/', include_in_schema=False)
async def directors_get_all(page: int = None, db: Session = Depends(get_db)):
    """
    Получить всех режиссеров
    """
    return DirectorService(session=db).get_all(page=page)


@router.get('/{pk}', summary='Получить режиссера по его ID')
async def directors_get_one(pk: int, db: Session = Depends(get_db)):
    """
    Получить режиссера по ID:

    - **pk**: ID режиссера
    """
    return DirectorService(db).get_one(pk)
