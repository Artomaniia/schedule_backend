"""init tables

Revision ID: 1a2b3c4d5e6f
Revises:
Create Date: 2026-02-10
"""

from alembic import op
import sqlalchemy as sa

revision = "1a2b3c4d5e6f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "disciplines",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=255), nullable=False, unique=True),
    )

    op.create_table(
        "weekdays",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=2), nullable=False),
        sa.UniqueConstraint("name", name="uq_weekdays_name"),
    )

    op.create_table(
        "teachers",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("discipline_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["discipline_id"],
            ["disciplines.id"],
            ondelete="RESTRICT",
        ),
    )
    op.create_index("ix_teachers_discipline_id", "teachers", ["discipline_id"])

    op.create_table(
        "weekday_disciplines",
        sa.Column("weekday_id", sa.Integer(), nullable=False),
        sa.Column("discipline_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["weekday_id"], ["weekdays.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["discipline_id"], ["disciplines.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("weekday_id", "discipline_id"),
    )


def downgrade() -> None:
    op.drop_table("weekday_disciplines")
    op.drop_index("ix_teachers_discipline_id", table_name="teachers")
    op.drop_table("teachers")
    op.drop_table("weekdays")
    op.drop_table("disciplines")
