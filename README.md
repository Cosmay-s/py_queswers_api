# py_queswers_ap#

## PyQueswers API

API сервис для вопросов и ответов на FastAPI

## Функциональность

- Создание и управление вопросами
- Добавление ответов к вопросам
- Каскадное удаление ответов при удалении вопроса

## Технологии

- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Alembic
- Docker

## Запуск

```bash
# Локально
uvicorn app.main:app --reload

# Через Docker
docker-compose up --build