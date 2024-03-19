"""add foreign key to books table

Revision ID: c103426a7d0b
Revises: ec80a04d246e
Create Date: 2024-03-19 15:39:10.142020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c103426a7d0b'
down_revision: Union[str, None] = 'ec80a04d246e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('books', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('books_users_fk', source_table='books', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')

def downgrade() -> None:
    op.drop_constraint('books_users_fk', table_name='books')
    op.drop_column('books', 'owner_id')
