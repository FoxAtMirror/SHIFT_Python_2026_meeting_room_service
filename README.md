# Meeting Room Service

## Возможности

* Регистрация пользователей
* Авторизация через JWT
* Получение информации о текущем пользователе
* Создание переговорных комнат
* Создание временных слотов для переговорных комнат
* Бронирование переговорных комнат на выбранную дату и временной слот
* Просмотр собственных бронирований
* Отмена бронирований
* Просмотр доступности переговорной комнаты на выбранную дату
* Разграничение прав пользователей (employee / admin)

---

## Технологии

* Python 3.12
* FastAPI
* SQLAlchemy
* PostgreSQL
* Poetry
* Docker
* Docker Compose
* Pytest

---

## Структура проекта

```text
app/
├── api/          # HTTP-эндпоинты
├── core/         # Безопасность и зависимости
├── db/           # Модели и работа с БД
├── schemas/      # Pydantic-схемы
├── services/     # Бизнес-логика
└── main.py

tests/
```

---

## Запуск локально

### Установка зависимостей

```bash
poetry install
```

### Запуск приложения

```bash
poetry run uvicorn app.main:app --reload
```

После запуска документация Swagger будет доступна по адресу:

```text
http://localhost:8000/docs
```

---

## Запуск через Docker

Сборка и запуск:

```bash
docker compose up --build
```

После запуска:

```text
http://localhost:8000/docs
```

Для остановки контейнеров:

```bash
docker compose down
```

Для полного удаления данных PostgreSQL:

```bash
docker compose down -v
```

---

## Аутентификация

### Регистрация

```http
POST /auth/register
```

Пример запроса:

```json
{
  "login": "user1",
  "password": "12345"
}
```

### Вход

```http
POST /auth/login
```

После успешной авторизации возвращается JWT-токен:

```json
{
  "access_token": "<jwt-token>",
  "token_type": "bearer"
}
```

Полученный токен используется для доступа к защищённым эндпоинтам.

---

## Основные эндпоинты

### Пользователи

| Метод | URL            |
| ----- | -------------- |
| POST  | /auth/register |
| POST  | /auth/login    |
| GET   | /auth/me       |

### Переговорные комнаты

| Метод | URL                           |
| ----- | ----------------------------- |
| GET   | /rooms                        |
| POST  | /rooms                        |
| GET   | /rooms/{room_id}/availability |

### Временные слоты

| Метод | URL                   |
| ----- | --------------------- |
| POST  | /slots                |
| GET   | /slots/room/{room_id} |

### Бронирования

| Метод  | URL                    |
| ------ | ---------------------- |
| POST   | /bookings              |
| GET    | /bookings              |
| GET    | /bookings/my           |
| DELETE | /bookings/{booking_id} |

---

## Тестирование

Запуск тестов:

```bash
poetry run pytest
```

---

## База данных

Для хранения данных используется PostgreSQL.

В базе данных хранятся:

* пользователи;
* переговорные комнаты;
* временные слоты;
* бронирования.

Взаимодействие с базой данных реализовано через SQLAlchemy.

---

## Автор

Vladislav Mikhalko
