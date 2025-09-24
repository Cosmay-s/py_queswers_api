from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, field_validator


class QuestionBase(BaseModel):
    text: str = Field(min_length=5,
                      max_length=1000,
                      description="Текст вопроса (5-1000 символов)")

    @field_validator('text')
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Текст вопроса не может быть пустым')
        # Убираем лишние пробелы и проверяем минимальную длину
        cleaned_text = ' '.join(v.strip().split())
        if len(cleaned_text) < 5:
            raise ValueError(
                'Текст вопроса должен содержать не менее 5 символов'
                )
        return cleaned_text


class QuestionCreate(QuestionBase):
    pass


class Question(QuestionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Импортируем Answer после определения Question
# (для избежания циклического импорта)
from app.schemas.answer import Answer


class QuestionWithAnswers(Question):
    answers: List[Answer] = []

    class Config:
        from_attributes = True
