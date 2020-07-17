"""empty message

Revision ID: 71a3751477e9
Revises: 40bf09a7fe15
Create Date: 2020-06-24 21:10:02.793238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71a3751477e9'
down_revision = '40bf09a7fe15'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('loser_id', sa.Integer(), nullable=True))
    op.add_column('games', sa.Column('venue', sa.String(), nullable=True))
    op.add_column('games', sa.Column('winner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'games', 'players', ['loser_id'], ['id'])
    op.create_foreign_key(None, 'games', 'players', ['winner_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'games', type_='foreignkey')
    op.drop_constraint(None, 'games', type_='foreignkey')
    op.drop_column('games', 'winner_id')
    op.drop_column('games', 'venue')
    op.drop_column('games', 'loser_id')
    # ### end Alembic commands ###
