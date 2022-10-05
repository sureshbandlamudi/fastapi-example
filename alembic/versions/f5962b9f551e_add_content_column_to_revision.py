"""Add Content Column to revision

Revision ID: f5962b9f551e
Revises: 3df43cb4f945
Create Date: 2022-09-30 16:05:43.255533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5962b9f551e'
down_revision = '3df43cb4f945'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
