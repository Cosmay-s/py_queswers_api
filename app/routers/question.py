from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.question import Question, QuestionCreate, QuestionWithAnswers
from app.schemas.answer import Answer, AnswerCreate
from app.services import QuestionService, AnswerService

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=List[Question])
def read_questions(
    skip: int = Query(0, description="Количество записей для пропуска"),
    limit: int = Query(100, description="Лимит записей", le=100),
    db: Session = Depends(get_db)
):
    """Получить список вопросов"""
    return QuestionService.get_questions(db, skip=skip, limit=limit)


@router.get("/{question_id}", response_model=QuestionWithAnswers)
def read_question(question_id: int, db: Session = Depends(get_db)):
    """Получить вопрос по ID с ответами"""
    return QuestionService.get_question(db, question_id)


@router.post("/", response_model=Question, status_code=status.HTTP_201_CREATED)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    """Создать новый вопрос"""
    return QuestionService.create_question(db, question)


@router.post("/{question_id}/answers",
             response_model=Answer,
             status_code=status.HTTP_201_CREATED)
def create_answer_for_question(question_id: int,
                               answer: AnswerCreate,
                               db: Session = Depends(get_db)):
    """Создать ответ для конкретного вопроса"""
    return AnswerService.create_answer(db, question_id, answer)


@router.delete("/{question_id}", status_code=status.HTTP_200_OK)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    """Удалить вопрос по ID (с каскадным удалением ответов)"""
    return QuestionService.delete_question(db, question_id)
