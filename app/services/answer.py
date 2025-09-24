from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.question import Question
from app.models.answer import Answer
from app.schemas.answer import AnswerCreate
from app.utils.logger import get_logger

logger = get_logger()


class AnswerService:
    @staticmethod
    def get_answer(db: Session, answer_id: int):
        """Получить ответ по ID"""
        logger.debug(f"Поиск ответа с ID: {answer_id}")
        stmt = select(Answer).where(Answer.id == answer_id)
        result = db.execute(stmt)
        answer = result.scalar_one_or_none()

        if answer is None:
            logger.warning(f"Ответ с ID {answer_id} не найден")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Answer not found"
            )

        logger.debug(
            f"Найден ответ ID {answer.id} для вопроса ID {answer.question_id}"
            )
        return answer

    @staticmethod
    def create_answer(db: Session, question_id: int, answer: AnswerCreate):
        """Создать ответ для вопроса"""
        logger.info(
            f"Создание ответа для вопроса ID {question_id} от {answer.user_id}"
            )

        # Проверяем существование вопроса
        question_stmt = select(Question).where(Question.id == question_id)
        result = db.execute(question_stmt)
        question = result.scalar_one_or_none()

        if question is None:
            logger.warning(f"Попытка создать ответ для несуществующего вопроса ID {question_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )

        # Проверяем длину ответа
        if len(answer.text) > 2000:
            logger.warning(
                f"Слишком длинный ответ: {len(answer.text)} символов"
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Answer text is too long (max 2000 characters)"
            )

        db_answer = Answer(
            question_id=question_id,
            text=answer.text,
            user_id=answer.user_id
        )
        db.add(db_answer)
        db.commit()
        db.refresh(db_answer)
        logger.info(
            f"Создан ответ с ID: {db_answer.id} для вопроса ID {question_id}"
            )
        return db_answer

    @staticmethod
    def delete_answer(db: Session, answer_id: int):
        """Удалить ответ по ID"""
        logger.info(f"Удаление ответа с ID: {answer_id}")
        answer = AnswerService.get_answer(db, answer_id)
        db.delete(answer)
        db.commit()
        logger.info(f"Удален ответ ID {answer_id}")
        return {"message": "Answer deleted successfully"}
