"""Add default timestamps to Review model

Revision ID: d108297831c7
Revises: 24bbeb3bd03f
Create Date: 2024-11-09 20:57:16.157075

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd108297831c7'
down_revision: Union[str, None] = '24bbeb3bd03f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('offers', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('reviews', 'offer_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('reviews', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('reviews', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reviews', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('reviews', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('reviews', 'offer_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('offers', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###