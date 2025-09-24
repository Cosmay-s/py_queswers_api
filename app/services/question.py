from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.question import Question
from app.schemas.question import QuestionCreate
from app.utils.logger import get_logger

logger = get_logger()


class QuestionService:
    @staticmethod
    def get_questions(db: Session, skip: int = 0, limit: int = 100):
        """Получить список вопросов с пагинацией"""
        logger.info(f"Получение списка вопросов: skip={skip}, limit={limit}")
        stmt = select(Question).offset(skip).limit(limit)
        result = db.execute(stmt)
        questions = result.scalars().all()
        logger.info(f"Найдено вопросов: {len(questions)}")
        return questions

    @staticmethod
    def get_question(db: Session, question_id: int):
        """Получить вопрос по ID с ответами"""
        logger.debug(f"Поиск вопроса с ID: {question_id}")
        stmt = select(Question).where(
            Question.id == question_id).options(
                selectinload(Question.answers)
                )
        result = db.execute(stmt)
        question = result.scalar_one_or_none()

        if question is None:
            logger.warning(f"Вопрос с ID {question_id} не найден")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )

        logger.debug(
            f"Найден вопрос ID {question.id} с {len(question.answers)}"
            )
        return question

    @staticmethod
    def create_question(db: Session, question: QuestionCreate):
        """Создать новый вопрос"""
        logger.info(f"Создание нового вопроса: {question.text[:50]}...")

        # Проверяем на дубликаты
        cleaned_text = ' '.join(question.text.strip().split()).lower()

        stmt = select(Question)
        result = db.execute(stmt)
        existing_questions = result.scalars().all()

        for existing_question in existing_questions:
            existing_text_cleaned = ' '.join(
                existing_question.text.strip().split()).lower()
            if existing_text_cleaned == cleaned_text:
                logger.warning(
                    f"Попытка создать дубликат вопроса: {question.text[:30]}"
                    )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Question with similar text already exists"
                )

        db_question = Question(text=question.text)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        logger.info(f"Создан вопрос с ID: {db_question.id}")
        return db_question

    @staticmethod
    def delete_question(db: Session, question_id: int):
        """Удалить вопрос по ID (каскадное удаление ответов)"""
        logger.info(f"Удаление вопроса с ID: {question_id}")
        question = QuestionService.get_question(db, question_id)
        answers_count = len(question.answers)
        db.delete(question)
        db.commit()
        logger.info(
            f"Удален вопрос ID {question_id} с {answers_count} ответами"
            )
        return {"message": "Question deleted successfully"}
