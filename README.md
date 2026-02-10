# Schedule Backend (FastAPI + MySQL + SQLAlchemy + Alembic)

## 1) Запуск MySQL (вариант с Docker)
```bash
docker compose up -d
```

## 2) Настройка окружения
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

pip install -r requirements.txt
cp .env.example .env
```

## 3) Применить миграции (создание таблиц + seed данные)
```bash
alembic upgrade head
```

## 4) Запуск приложения
```bash
uvicorn app.main:app --reload
```

Swagger:
- http://127.0.0.1:8000/docs

---

## Что получится в Swagger

- `POST/GET/PUT/DELETE /disciplines`
- `POST/GET/PUT/DELETE /teachers` (в ответе teacher возвращается с вложенной дисциплиной)
- `POST/GET/PUT/DELETE /weekdays` (в запросах `discipline_ids`, в ответе — список дисциплин)

---

Если хочешь, могу:
- добавить **поиск/фильтры** (например, “получить расписание на день по `name=пн`”),
- сделать **эндпоинт “получить расписание на неделю”** в удобном виде,
- или добавить сущность **пара (время/аудитория)**, если тебе нужно именно “расписание занятий” по слотам.
