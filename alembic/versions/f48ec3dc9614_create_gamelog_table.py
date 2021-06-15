"""create gamelog table

Revision ID: f48ec3dc9614
Revises: 8229c7653952
Create Date: 2021-06-14 21:59:54.789718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f48ec3dc9614'
down_revision = '8229c7653952'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'gamelog',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('date', sa.String(50), nullable=False),
        sa.Column('position', sa.String(50), nullable=False),
    )

def downgrade():
    op.drop_table('gamelog')
