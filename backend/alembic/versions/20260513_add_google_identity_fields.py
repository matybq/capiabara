"""add_google_identity_fields

Revision ID: 20260513a001
Revises: e8e2ba3b6364
Create Date: 2026-05-13 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260513a001"
down_revision: Union[str, Sequence[str], None] = "e8e2ba3b6364"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add nullable columns first so existing rows are not broken
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(sa.Column("email", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("google_sub", sa.String(), nullable=True))
        batch_op.add_column(
            sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true())
        )

    # Enforce uniqueness after columns exist
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.create_unique_constraint("uq_users_email", ["email"])
        batch_op.create_unique_constraint("uq_users_google_sub", ["google_sub"])


def downgrade() -> None:
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_constraint("uq_users_google_sub", type_="unique")
        batch_op.drop_constraint("uq_users_email", type_="unique")
        batch_op.drop_column("is_active")
        batch_op.drop_column("google_sub")
        batch_op.drop_column("email")
