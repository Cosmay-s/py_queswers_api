from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class AnswerBase(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=2000,
        description="Текст ответа",
        )

    user_id: str = Field(
        min_length=1,
        max_length=255,
        description="ID пользователя",
        )

    @field_validator('text')
    def text_cannot_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Текст ответа не может быть пустым')
        return v.strip()

    @field_validator('user_id')
    def user_id_cannot_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('ID пользователя не может быть пустым')
        return v.strip()


class AnswerCreate(AnswerBase):
    pass


class Answer(AnswerBase):
    id: int
    question_id: int
    created_at: datetime

    class Config:
        from_attributes = True
