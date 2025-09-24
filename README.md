## PyQueswers API

API-сервис для управления вопросами и ответами, реализованный на FastAPI.

## Функциональность

- Создание, получение, удаление вопросов
- Добавление, получение, удаление ответов к вопросам
- Каскадное удаление ответов при удалении вопроса
- Валидация входных данных
- Поддержка нескольких ответов на вопрос от одного пользователя

## Технологии

- **FastAPI** - современный фреймворк для API
- **SQLAlchemy 2.0** - ORM для работы с базой данных
- **PostgreSQL** - реляционная база данных
- **Pydantic** - валидация и сериализация данных
- **Alembic** - система миграций базы данных
- **Docker & Docker Compose** - контейнеризация и оркестрация
- **Loguru** - простое и эффективное логирование

## API Endpoints

### Вопросы
- `GET /api/v1/questions/` - список всех вопросов
- `POST /api/v1/questions/` - создать новый вопрос
- `GET /api/v1/questions/{id}` - получить вопрос с ответами
- `DELETE /api/v1/questions/{id}` - удалить вопрос (с ответами)

### Ответы
- `POST /api/v1/answers/questions/{id}/answers/` - добавить ответ к вопросу
- `GET /api/v1/answers/{id}` - получить ответ по ID
- `DELETE /api/v1/answers/{id}` - удалить ответ

## Быстрый старт

### Запуск через Docker

```bash
# Клонировать репозиторий
git clone https://github.com/Cosmay-s/py_queswers_api.git
cd py_queswers_api

# Запустить приложение
docker-compose up --build
```

Приложение будет доступно по адресу: http://localhost:8000

### Локальная разработка

```bash
# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt

# Запустить сервер
uvicorn app.main:app --reload
```

## Миграции

```bash
# Создать новую миграцию
alembic revision --autogenerate -m "Описание изменений"

# Применить миграции
alembic upgrade head

# Откатить последнюю миграцию
alembic downgrade -1
```

## Тестирование

```bash
python -m pytest tests/test_api.py -v
python -m pytest tests/test_validation.py -v
python -m pytest tests/test_business_rules.py -v
```

## Документация

После запуска приложения доступна автоматическая документация:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Структура проекта

```
py_queswers_ap/
├── app/                    # Основное приложение
│   ├── models/            # Модели SQLAlchemy
│   ├── schemas/           # Pydantic схемы
│   ├── routers/           # Маршруты API
│   ├── services/          # Бизнес-логика
│   ├── utils/             # Вспомогательные функции
│   ├── main.py            # Точка входа
│   ├── config.py          # Конфигурация
│   └── database.py        # Настройка БД
├── tests/                 # Тесты
├── migrations/            # Миграции Alembic
├── logs/                  # Логи приложения
├── docker-compose.yml     # Docker Compose
├── Dockerfile            # Образ приложения
└── requirements.txt      # Зависимости Python
```

## Особенности реализации

- **Модульная архитектура** - разделение на модели, схемы, роутеры и сервисы
- **Валидация данных** - строгая проверка входных данных с помощью Pydantic
- **Каскадное удаление** - автоматическое удаление ответов при удалении вопроса
- **Логирование** - детальное логирование операций с помощью Loguru
- **Контейнеризация** - полная поддержка Docker для легкого развертывания