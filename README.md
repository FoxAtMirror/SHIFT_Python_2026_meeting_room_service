# Meeting Room Booking Service

Сервис бронирования переговорных комнат, разработанный на FastAPI в рамках тестового задания.

## Функциональность

### Сотрудник

* Регистрация и авторизация
* Просмотр списка переговорных комнат
* Просмотр доступных временных слотов для выбранной комнаты
* Создание бронирования
* Просмотр своих бронирований
* Отмена собственных бронирований

### Администратор

Дополнительно к возможностям сотрудника:

* Создание переговорных комнат
* Создание временных слотов
* Просмотр всех бронирований
* Отмена любых бронирований

## Технологии

* Python 3.12
* FastAPI
* SQLAlchemy
* PostgreSQL
* JWT Authentication
* Pytest
* Docker
* Docker Compose
* Vanilla JavaScript

## Запуск через Docker

### 1. Клонировать репозиторий

```bash
git clone https://github.com/FoxAtMirror/SHIFT_Python_2026_meeting_room_service.git
cd SHIFT_Python_2026_meeting_room_service
```

### 2. Создать файл .env и .env.docker

Создать ./backend/.env прописать секретный ключ, ДБ URL и Тест ДБ URL для локального запуска

```bash
MEETING_ROOM_SERVICE_SECRET_KEY=MEETING_ROOM_SERVICE_SECRET_KEY
DATABASE_URL=postgresql://postgres:0000@localhost:5432/meeting_room
TEST_DATABASE_URL=postgresql://postgres:0000@localhost:5432/meeting_room_test
```

И соответственно для .env.docker

```bash
MEETING_ROOM_SERVICE_SECRET_KEY=MEETING_ROOM_SERVICE_SECRET_KEY
DATABASE_URL=postgresql://postgres:0000@db:5432/meeting_room
TEST_DATABASE_URL=postgresql://postgres:0000@db:5432/meeting_room_test
```

### 3. Запустить приложение

```bash
docker compose up --build
```

После запуска будут доступны:

Swagger UI:

```text
http://localhost:8000/docs
```

Frontend:

```text
http://localhost:5500/pages/login.html
```

## Тестовый администратор

При запуске приложения автоматически создаётся пользователь администратора.

Логин:

```text
admin
```

Пароль:

```text
admin
```

## Запуск тестов

Из директории backend:

```bash
poetry install
poetry run pytest
```

## Основные API эндпоинты

### Авторизация

```http
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
```

### Комнаты

```http
GET  /api/rooms
POST /api/rooms
GET  /api/rooms/{room_id}/availability
```

### Слоты

```http
POST /api/slots
GET  /api/slots/room/{room_id}
```

### Бронирования

```http
POST   /api/bookings
GET    /api/bookings/my
GET    /api/bookings
DELETE /api/bookings/{booking_id}
```

## Примеры работы

### Регистрация пользователя

Пользователь открывает страницу регистрации:

```text
http://localhost:5500/pages/register.html
```

![Авторизация](screenshots/login.png)

После успешной регистрации выполняется автоматический вход в систему.

### Просмотр комнат

После авторизации пользователь видит список доступных переговорных комнат.

![Список комнат](screenshots/rooms.png)

### Создание бронирования

1. Открыть страницу комнаты.
2. Выбрать дату.
3. Выбрать свободный слот.
4. Нажать кнопку "Забронировать".

![Создание бронирования](screenshots/room-details.png)


### Просмотр своих бронирований

На странице "Мои бронирования" пользователь может увидеть все свои активные бронирования и отменить любое из них.

![Просмотр бронирования](screenshots/my-bookings.png)

### Администрирование

Администратор может:

* создавать комнаты;
* создавать слоты;
* просматривать все бронирования;
* отменять любые бронирования пользователей.

![Панель администратора](screenshots/admin-panel.png)

## Дополнительные проверки

Реализованы следующие ограничения:

* нельзя бронировать прошедшие даты;
* нельзя создать пересекающиеся временные слоты для одной комнаты;
* нельзя создать бронирование для уже занятого слота;
* сотрудник не может удалить бронирование другого пользователя;
* администратор может удалить любое бронирование.
