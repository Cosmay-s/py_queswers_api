from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, field_validator


class QuestionBase(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Текст вопроса",
        )

    @field_validator('text')
    def text_cannot_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Текст вопроса не может быть пустым')
        return v.strip()


class QuestionCreate(QuestionBase):
    pass


class Question(QuestionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionWithAnswers(Question):
    answers: List['Answer'] = []

    class Config:
        from_attributes = True
