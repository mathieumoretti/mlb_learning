"""create player table

Revision ID: a1703b7bfc36
Revises: 
Create Date: 2021-02-10 00:09:52.380847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1703b7bfc36'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'player',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
    )

def downgrade():
    op.drop_table('player')
