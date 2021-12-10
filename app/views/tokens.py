from fastapi import APIRouter, Depends
from app.service.rtokens import RTokenService
from app.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix='/tokens', tags=['tokens'])


@router.get('', summary='Получить все токены из базы')
async def tokens_get_all(db: Session = Depends(get_db)):
    """
    Получить все токены из базы
    """
    return RTokenService(session=db).get_all()
