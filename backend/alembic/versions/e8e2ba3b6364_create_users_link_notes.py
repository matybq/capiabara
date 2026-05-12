"""create_users_link_notes

Revision ID: e8e2ba3b6364
Revises: edf962dd00cb
Create Date: 2026-05-12 14:26:14.082385

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8e2ba3b6364'
down_revision: Union[str, Sequence[str], None] = 'edf962dd00cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    # SQLite does not support ALTER COLUMN or ADD CONSTRAINT after creation.
    # batch_alter_table recreates the table to apply the changes.
    with op.batch_alter_table('notes', schema=None) as batch_op:
        batch_op.alter_column(
            'user_id',
            existing_type=sa.VARCHAR(),
            type_=sa.Integer(),
            existing_nullable=False,
        )
        batch_op.create_foreign_key(
            'fk_notes_user_id_users', 'users', ['user_id'], ['id']
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('notes', schema=None) as batch_op:
        batch_op.drop_constraint('fk_notes_user_id_users', type_='foreignkey')
        batch_op.alter_column(
            'user_id',
            existing_type=sa.Integer(),
            type_=sa.VARCHAR(),
            existing_nullable=False,
        )
    op.drop_table('users')
