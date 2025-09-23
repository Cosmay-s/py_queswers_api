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
```

## Работа с миграциями

```bash
# Создание новой миграции
alembic revision --autogenerate -m "..."

# Применение миграции
alembic upgrade head

# Откат последней миграции
alembic downgrade -1
```