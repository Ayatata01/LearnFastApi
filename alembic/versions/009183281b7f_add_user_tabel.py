"""add user tabel

Revision ID: 009183281b7f
Revises: 37a01f5bb907
Create Date: 2022-07-15 21:13:27.141809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '009183281b7f'
down_revision = '37a01f5bb907'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default = sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )   
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
