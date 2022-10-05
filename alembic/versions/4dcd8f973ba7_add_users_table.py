"""Add Users table

Revision ID: 4dcd8f973ba7
Revises: f5962b9f551e
Create Date: 2022-09-30 16:10:26.560175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4dcd8f973ba7'
down_revision = 'f5962b9f551e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',sa.Column('id',sa.Integer(), nullable=False),
                            sa.Column('email',sa.String(),nullable=False),
                            sa.Column('password',sa.String,nullable=False),
                            sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()'),nullable=False),
                            sa.PrimaryKeyConstraint('id'),
                            sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
