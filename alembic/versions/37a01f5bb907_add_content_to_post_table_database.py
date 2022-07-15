"""add content to post table database

Revision ID: 37a01f5bb907
Revises: 4efdde96f985
Create Date: 2022-07-15 21:05:10.189096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37a01f5bb907'
down_revision = '4efdde96f985'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
