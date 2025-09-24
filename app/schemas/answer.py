from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class AnswerBase(BaseModel):
    text: str = Field(min_length=3,
                      max_length=2000,
                      description="Текст ответа (3-2000 символов)")

    user_id: str = Field(min_length=1,
                         max_length=255,
                         description="ID пользователя")

    @field_validator('text')
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Текст ответа не может быть пустым')
        cleaned_text = ' '.join(v.strip().split())
        if len(cleaned_text) < 3:
            raise ValueError(
                'Текст ответа должен содержать не менее 3 символов'
                )
        return cleaned_text

    @field_validator('user_id')
    def validate_user_id(cls, v):
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
