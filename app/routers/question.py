from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.question import Question, QuestionCreate, QuestionWithAnswers
from app.services import QuestionService

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=List[Question])
def read_questions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    db: Session = Depends(get_db)
):
    """Запросить все Questions, вернуть список схем Question"""
    return QuestionService.get_questions(db, skip=skip, limit=limit)


@router.post("/", response_model=Question, status_code=status.HTTP_201_CREATED)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    """Создать Question из QuestionCreate, добавить в БД, вернуть Question"""
    return QuestionService.create_question(db, question)


@router.get("/{question_id}", response_model=QuestionWithAnswers)
def read_question(question_id: int, db: Session = Depends(get_db)):
    """Получить Question по id, включить answers"""
    return QuestionService.get_question(db, question_id)


@router.delete("/{question_id}", status_code=status.HTTP_200_OK)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    """Удалить Question по id (каскадное удаление answers)"""
    return QuestionService.delete_question(db, question_id)
