from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.answer import Answer
from app.services import AnswerService

router = APIRouter(prefix="/answers", tags=["answers"])


@router.get("/{answer_id}", response_model=Answer)
def read_answer(answer_id: int, db: Session = Depends(get_db)):
    """Получить ответ по ID"""
    return AnswerService.get_answer(db, answer_id)


@router.delete("/{answer_id}", status_code=status.HTTP_200_OK)
def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    """Удалить ответ по ID"""
    return AnswerService.delete_answer(db, answer_id)
