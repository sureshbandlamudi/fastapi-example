"""Create posts table

Revision ID: 3df43cb4f945
Revises: 
Create Date: 2022-09-30 15:57:13.706229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3df43cb4f945'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts",sa.Column('id', sa.Integer(), nullable = False, primary_key=True),
    sa.Column('title', sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
