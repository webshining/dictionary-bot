"""Add word learning progress.

Revision ID: b5a6c7d8e9f0
Revises: ca787e744366
Create Date: 2026-09-25

"""

import sqlalchemy as sa
from alembic import op

revision: str = "b5a6c7d8e9f0"
down_revision: str | None = "ca787e744366"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("user_words", sa.Column("repetitions", sa.Integer(), server_default="0", nullable=False))
    op.add_column("user_words", sa.Column("lapses", sa.Integer(), server_default="0", nullable=False))
    op.add_column("user_words", sa.Column("interval_days", sa.Integer(), server_default="0", nullable=False))
    op.add_column("user_words", sa.Column("ease_factor", sa.Float(), server_default="2.5", nullable=False))
    op.add_column("user_words", sa.Column("due_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("user_words", sa.Column("last_reviewed_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("user_words", "last_reviewed_at")
    op.drop_column("user_words", "due_at")
    op.drop_column("user_words", "ease_factor")
    op.drop_column("user_words", "interval_days")
    op.drop_column("user_words", "lapses")
    op.drop_column("user_words", "repetitions")
