"""Add Approve

Revision ID: 53770cf61da5
Revises: 298454282051
Create Date: 2024-09-15 09:37:12.213634

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53770cf61da5'
down_revision: Union[str, None] = '298454282051'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('approves',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_approved', sa.Boolean(), nullable=True),
    sa.Column('approved_by', sa.String(length=255), nullable=True),
    sa.Column('approved_at', sa.DateTime(), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('created_by', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.String(length=255), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_approves_id'), 'approves', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_approves_id'), table_name='approves')
    op.drop_table('approves')
    # ### end Alembic commands ###