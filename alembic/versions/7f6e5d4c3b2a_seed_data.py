"""seed data

Revision ID: 7f6e5d4c3b2a
Revises: 1a2b3c4d5e6f
Create Date: 2026-02-10
"""

from alembic import op
import sqlalchemy as sa

revision = "7f6e5d4c3b2a"
down_revision = "1a2b3c4d5e6f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    disciplines = sa.table(
        "disciplines",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
    )
    teachers = sa.table(
        "teachers",
        sa.column("id", sa.Integer),
        sa.column("full_name", sa.String),
        sa.column("discipline_id", sa.Integer),
    )
    weekdays = sa.table(
        "weekdays",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
    )
    weekday_disciplines = sa.table(
        "weekday_disciplines",
        sa.column("weekday_id", sa.Integer),
        sa.column("discipline_id", sa.Integer),
    )

    # Дисциплины (фиксируем id, чтобы легко связать)
    op.bulk_insert(
        disciplines,
        [
            {"id": 1, "name": "Математика"},
            {"id": 2, "name": "Программирование"},
            {"id": 3, "name": "Физика"},
            {"id": 4, "name": "История"},
        ],
    )

    # Преподаватели
    op.bulk_insert(
        teachers,
        [
            {"id": 1, "full_name": "Иванов Иван Иванович", "discipline_id": 1},
            {"id": 2, "full_name": "Петров Пётр Петрович", "discipline_id": 2},
            {"id": 3, "full_name": "Сидорова Анна Сергеевна", "discipline_id": 3},
            {"id": 4, "full_name": "Кузнецов Дмитрий Олегович", "discipline_id": 4},
        ],
    )

    # Дни недели
    op.bulk_insert(
        weekdays,
        [
            {"id": 1, "name": "пн"},
            {"id": 2, "name": "вт"},
            {"id": 3, "name": "ср"},
            {"id": 4, "name": "чт"},
            {"id": 5, "name": "пт"},
            {"id": 6, "name": "сб"},
            {"id": 7, "name": "вс"},
        ],
    )

    # Связи день -> дисциплины
    op.bulk_insert(
        weekday_disciplines,
        [
            {"weekday_id": 1, "discipline_id": 1},
            {"weekday_id": 1, "discipline_id": 2},
            {"weekday_id": 2, "discipline_id": 3},
            {"weekday_id": 3, "discipline_id": 2},
            {"weekday_id": 4, "discipline_id": 4},
            {"weekday_id": 5, "discipline_id": 1},
            {"weekday_id": 6, "discipline_id": 3},
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM weekday_disciplines")
    op.execute("DELETE FROM teachers")
    op.execute("DELETE FROM weekdays")
    op.execute("DELETE FROM disciplines")
