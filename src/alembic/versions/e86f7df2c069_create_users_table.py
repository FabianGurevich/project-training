"""create users table

Revision ID: e86f7df2c069
Revises: 
Create Date: 2024-08-26 15:33:34.909242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e86f7df2c069'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    sa.Table(
        'users',
        sa.MetaData(),
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
    )


def downgrade():
    op.drop_table('users')
