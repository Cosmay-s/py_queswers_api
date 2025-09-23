from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.question import Question
from app.models.answer import Answer
from app.schemas.answer import AnswerCreate


class AnswerService:
    @staticmethod
    def get_answer(db: Session, answer_id: int):
        """Получить ответ по ID"""
        stmt = select(Answer).where(Answer.id == answer_id)
        result = db.execute(stmt)
        answer = result.scalar_one_or_none()

        if answer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Answer not found"
            )
        return answer

    @staticmethod
    def create_answer(db: Session, question_id: int, answer: AnswerCreate):
        """Создать ответ для вопроса"""
        question_stmt = select(Question).where(Question.id == question_id)
        result = db.execute(question_stmt)
        question = result.scalar_one_or_none()

        if question is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )

        db_answer = Answer(
            question_id=question_id,
            text=answer.text,
            user_id=answer.user_id
        )
        db.add(db_answer)
        db.commit()
        db.refresh(db_answer)
        return db_answer

    @staticmethod
    def delete_answer(db: Session, answer_id: int):
        """Удалить ответ по ID"""
        answer = AnswerService.get_answer(db, answer_id)
        db.delete(answer)
        db.commit()
        return {"message": "Answer deleted successfully"}
