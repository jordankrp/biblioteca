"""add author, summary and year to books table

Revision ID: 6746f7bb4094
Revises: dc2ceb1523df
Create Date: 2024-03-13 17:45:33.024158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6746f7bb4094'
down_revision: Union[str, None] = 'dc2ceb1523df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('books', sa.Column('author', sa.String(), nullable=False))
    op.add_column('books', sa.Column('year', sa.Integer(), nullable=False))
    op.add_column('books', sa.Column('summary', sa.String()))
    op.add_column('books', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))


def downgrade() -> None:
    op.drop_column('books', 'author')
    op.drop_column('books', 'year')
    op.drop_column('books', 'summary')
    op.drop_column('books', 'created_at')

