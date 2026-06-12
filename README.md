# Meeting Room Service

## Функциональность

* Регистрация пользователей
* Авторизация через JWT
* Получение информации о текущем пользователе
* Создание переговорных комнат
* Создание временных слотов
* Создание бронирований
* Просмотр собственных бронирований
* Отмена бронирований
* Просмотр доступности комнаты на выбранную дату
* Разграничение прав пользователей (employee / admin)

## Технологии

* Python 3.12
* FastAPI
* SQLAlchemy
* PostgreSQL
* Poetry
* Docker
* Docker Compose
* Pytest

## Запуск проекта через Docker

Сборка и запуск:

```bash
docker compose up --build
```

После запуска документация будет доступна по адресу:

http://localhost:8000/docs

## Локальный запуск

Установка зависимостей:

```bash
poetry install
```

Запуск приложения:

```bash
poetry run uvicorn app.main:app --reload
```

Документация:

http://localhost:8000/docs

## Запуск тестов

```bash
poetry run pytest
```

## Основные эндпоинты

### Авторизация

POST /auth/register

POST /auth/login

GET /auth/me

### Комнаты

GET /rooms

POST /rooms

GET /rooms/{room_id}/availability

### Слоты

POST /slots

GET /slots/room/{room_id}

### Бронирования

POST /bookings

GET /bookings

GET /bookings/my

DELETE /bookings/{booking_id}
