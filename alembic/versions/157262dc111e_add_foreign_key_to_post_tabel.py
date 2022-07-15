"""add foreign key to post tabel

Revision ID: 157262dc111e
Revises: 009183281b7f
Create Date: 2022-07-15 21:24:51.837706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '157262dc111e'
down_revision = '009183281b7f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False)),
    op.create_foreign_key('post_users_fkey', source_table='posts', referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete = "CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fkey', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
