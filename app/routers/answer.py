from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.answer import Answer, AnswerCreate
from app.services import AnswerService

router = APIRouter(prefix="/answers", tags=["answers"])


@router.post("/questions/{question_id}/answers/",
             response_model=Answer,
             status_code=status.HTTP_201_CREATED)
def create_answer(question_id: int,
                  answer: AnswerCreate,
                  db: Session = Depends(get_db)):
    """Проверить существование вопроса, создать Answer с question_id"""
    return AnswerService.create_answer(db, question_id, answer)


@router.get("/{answer_id}", response_model=Answer)
def read_answer(answer_id: int, db: Session = Depends(get_db)):
    """Получить Answer по id"""
    return AnswerService.get_answer(db, answer_id)


@router.delete("/{answer_id}", status_code=status.HTTP_200_OK)
def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    """Удалить Answer по id"""
    return AnswerService.delete_answer(db, answer_id)
