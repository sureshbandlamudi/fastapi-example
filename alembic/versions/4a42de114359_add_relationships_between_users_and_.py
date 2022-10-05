"""add relationships between users and posts using Foriegn key

Revision ID: 4a42de114359
Revises: 4dcd8f973ba7
Create Date: 2022-10-04 15:44:56.165066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a42de114359'
down_revision = '4dcd8f973ba7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk',source_table="posts",referent_table="users",local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk',table_name="posts")
    op.drop_column('posts','owner_id')
    pass
