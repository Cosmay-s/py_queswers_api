from sqlalchemy.orm import Session, selectinload
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
            Question.id == question_id).options(
                selectinload(Question.answers)
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
        """Создать новый вопрос с проверкой на дубликаты"""
        # Проверяем, нет ли уже похожего вопроса (игнорируя регистр и пробелы)
        cleaned_text = ' '.join(question.text.strip().split()).lower()

        stmt = select(Question)
        result = db.execute(stmt)
        existing_questions = result.scalars().all()

        for existing_question in existing_questions:
            existing_text_cleaned = ' '.join(
                existing_question.text.strip().split()
                ).lower()
            if existing_text_cleaned == cleaned_text:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Question with similar text already exists"
                )

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
