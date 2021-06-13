"""create statline table

Revision ID: 8229c7653952
Revises: a1703b7bfc36
Create Date: 2021-05-24 16:05:04.795568

"""
from alembic import op
import sqlalchemy as sa
# import os
# from os import SEEK_CUR, walk
# import sys

# script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
# root_dir = os.path.join(script_dir, '..')
# data_path = os.path.join(root_dir, 'data')

# sys.path.append(root_dir)

from mlb_learning.models import Categories

# revision identifiers, used by Alembic.
revision = '8229c7653952'
down_revision = 'a1703b7bfc36'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'statline',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(Categories.AIR_OUTS.name, sa.Integer, nullable=False),
        sa.Column(Categories.AT_BATS.name, sa.Integer, nullable=False),
        sa.Column(Categories.BALLS.name, sa.Integer, nullable=False),
        sa.Column(Categories.BASE_ON_BALLS.name, sa.Integer, nullable=False),
        sa.Column(Categories.BATTERS_FACED.name, sa.Integer, nullable=False),
        sa.Column(Categories.BLOWN_SAVES.name, sa.Integer, nullable=False),
        sa.Column(Categories.CATCHERS_INTERFERENCE.name, sa.Integer, nullable=False),
        sa.Column(Categories.CAUGHT_STEALING.name, sa.Integer, nullable=False),
        sa.Column(Categories.COMPLETE_GAMES.name, sa.Integer, nullable=False),
        sa.Column(Categories.DOUBLES.name, sa.Integer, nullable=False),
        sa.Column(Categories.EARNED_RUNS.name, sa.Integer, nullable=False),
        sa.Column(Categories.FLY_OUTS.name, sa.Integer, nullable=False),
        sa.Column(Categories.HOME_RUNS.name, sa.Integer, nullable=False),
        sa.Column(Categories.GAMES_FINISHED.name, sa.Integer, nullable=False),
        sa.Column(Categories.GAMES_PITCHED.name, sa.Integer, nullable=False),
        sa.Column(Categories.GAMES_PLAYED.name, sa.Integer, nullable=False),
        sa.Column(Categories.GAMES_STARTED.name, sa.Integer, nullable=False),
        sa.Column(Categories.GROUND_INTO_DOUBLE_PLAY.name, sa.Integer, nullable=False),
        sa.Column(Categories.GROUND_INTO_TRIPLE_PLAY.name, sa.Integer, nullable=False),
        sa.Column(Categories.GROUND_OUTS.name, sa.Integer, nullable=False),
        sa.Column(Categories.HITS.name, sa.Integer, nullable=False),
        sa.Column(Categories.HIT_BATSMEN.name, sa.Integer, nullable=False),
        sa.Column(Categories.HIT_BY_PITCH.name, sa.Integer, nullable=False),
        sa.Column(Categories.HOLDS.name, sa.Integer, nullable=False),
        sa.Column(Categories.INHERITED_RUNNERS.name, sa.Integer, nullable=False),
        sa.Column(Categories.INHRETIED_RUNNERS_SCORED.name, sa.Integer, nullable=False),
        sa.Column(Categories.INNINGS_PITCHED.name, sa.Integer, nullable=False),
        sa.Column(Categories.INTENTIONAL_WALKS.name, sa.Integer, nullable=False),
        sa.Column(Categories.LEFT_ON_BASE.name, sa.Integer, nullable=False),
        sa.Column(Categories.LOSSES.name, sa.Integer, nullable=False),
        sa.Column(Categories.NOTE.name, sa.String(256), nullable=False),
        sa.Column(Categories.NUMBER_OF_PITCHES.name, sa.Integer, nullable=False),
        sa.Column(Categories.OUTS.name, sa.Integer, nullable=False),
        sa.Column(Categories.PICKOFFS.name, sa.Integer, nullable=False),
        sa.Column(Categories.PITCHES_THROWN.name, sa.Integer, nullable=False),
        sa.Column(Categories.RBI.name, sa.Integer, nullable=False),
        sa.Column(Categories.RUNS.name, sa.Integer, nullable=False),
        sa.Column(Categories.SAVE_OPPORTUNITIES.name, sa.Integer, nullable=False),
        sa.Column(Categories.SAC_BUNTS.name, sa.Integer, nullable=False),
        sa.Column(Categories.SAC_FLIES.name, sa.Integer, nullable=False),
        sa.Column(Categories.SAVES.name, sa.Integer, nullable=False),
        sa.Column(Categories.SHUTOUTS.name, sa.Integer, nullable=False),
        sa.Column(Categories.STOLEN_BASES.name, sa.Integer, nullable=False),
        sa.Column(Categories.STRIKES.name, sa.Integer, nullable=False),
        sa.Column(Categories.STRIKE_OUTS.name, sa.Integer, nullable=False),
        sa.Column(Categories.TRIPLES.name, sa.Integer, nullable=False),
        sa.Column(Categories.TOTAL_BASES.name, sa.Integer, nullable=False),
        sa.Column(Categories.WILD_PITCHES.name, sa.Integer, nullable=False),
        sa.Column(Categories.WINS.name, sa.Integer, nullable=False),
    )

def downgrade():
    op.drop_table('statline')
