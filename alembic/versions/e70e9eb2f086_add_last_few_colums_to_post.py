"""add last few colums to post

Revision ID: e70e9eb2f086
Revises: 157262dc111e
Create Date: 2022-07-15 21:37:04.347586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e70e9eb2f086'
down_revision = '157262dc111e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default = 'TRUE')),
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone = True), server_default = sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
