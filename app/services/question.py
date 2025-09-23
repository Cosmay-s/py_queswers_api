from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.question import Question
from app.schemas.question import QuestionCreate


class QuestionService:
    @staticmethod
    def get_questions(db: Session, skip: int = 0, limit: int = 100):
        """Получить список вопросов с пагинацией"""
        stmt = select(Question).offset(skip).limit(limit)
        result = db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def get_question(db: Session, question_id: int):
        """Получить вопрос по ID с ответами"""
        stmt = select(Question).where(
            Question.id == question_id
                ).options(joinedload(Question.answers)
                          )
        result = db.execute(stmt)
        question = result.scalar_one_or_none()

        if question is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )
        return question

    @staticmethod
    def create_question(db: Session, question: QuestionCreate):
        """Создать новый вопрос"""
        db_question = Question(text=question.text)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        return db_question

    @staticmethod
    def delete_question(db: Session, question_id: int):
        """Удалить вопрос по ID (каскадное удаление ответов)"""
        question = QuestionService.get_question(db, question_id)
        db.delete(question)
        db.commit()
        return {"message": "Question deleted successfully"}
