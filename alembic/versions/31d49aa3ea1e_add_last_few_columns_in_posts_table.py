"""add last few columns in posts table

Revision ID: 31d49aa3ea1e
Revises: 4a42de114359
Create Date: 2022-10-04 15:50:05.360457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31d49aa3ea1e'
down_revision = '4a42de114359'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,server_default='True'))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
    pass
