# Riot Matches Service

Cервис, который тянет данные о матчах конкретного игрока из Riot API, складывает в Postgres и отдаёт наружу через свой read-only API.

#### Функциональность

- API:
    - ```POST /admin/players/{puuid}/update``` — Обновляет рейтинговые записи и историю матчей игрока.
    - ```POST /players/{game_name}/{tag_line}``` — Создает профиль игрока из API Riot, сохраняет/обновляет локальную базу данных и возвращает данные об игроке.
    - ```GET /players/{puuid}``` — Возвращает профиль игрока из БД с рейтинговыми записями игрока.
    - ```GET /players/{puuid}/champions``` — Возвращает сводную статистику игрока по титулам чемпиона.
    - ```GET /players/{puuid}/matches_participants``` — Возвращает статистику участия игрока в матче.
    - ```GET /players/{puuid}/matches``` — Возвращает последние матчи игрока.

## Match History Depth
По умолчанию Riot API возвращает последние 20 матчей (`count=20`).  
В сервисе используется такое же значение по умолчанию.
Riot API позволяет указать до 100 матчей.

## Stack
- Backend: Python, FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy
- Migrations: Alembic
- HTTP client: httpx
- Dependency manager: Poetry

## Необходимые технологии
- Python 3.13
- Poetry
- Docker and Docker Compose (optional)

## Установка
1. Клонируем репозиторий:
   ```
   git clone https://github.com/AKamysheva/match_history_service.git
   poetry install 
   ```
2. Создать .env файл в папке ```app```
   ```
   POSTGRES_USER=myuser
   POSTGRES_PASSWORD=mypassword
   POSTGRES_DB=mydatabase
   HOST_DB=db
   PORT_DB=5432
   API_RIOT_KEY=myapikey
   ```
3. Запускаем проект с Docker Compose:
   ```
   docker compose up -d
   ```

## API Documentation
👉 http://localhost:8500/docs