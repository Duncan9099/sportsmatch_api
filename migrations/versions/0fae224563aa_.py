"""empty message

Revision ID: 0fae224563aa
Revises: 71a3751477e9
Create Date: 2020-06-24 21:14:05.194087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fae224563aa'
down_revision = '71a3751477e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('lose_id', sa.Integer(), nullable=True))
    op.add_column('games', sa.Column('win_id', sa.Integer(), nullable=True))
    op.drop_constraint('games_winner_id_fkey', 'games', type_='foreignkey')
    op.drop_constraint('games_loser_id_fkey', 'games', type_='foreignkey')
    op.create_foreign_key(None, 'games', 'players', ['win_id'], ['id'])
    op.create_foreign_key(None, 'games', 'players', ['lose_id'], ['id'])
    op.drop_column('games', 'loser_id')
    op.drop_column('games', 'winner_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('winner_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('games', sa.Column('loser_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'games', type_='foreignkey')
    op.drop_constraint(None, 'games', type_='foreignkey')
    op.create_foreign_key('games_loser_id_fkey', 'games', 'players', ['loser_id'], ['id'])
    op.create_foreign_key('games_winner_id_fkey', 'games', 'players', ['winner_id'], ['id'])
    op.drop_column('games', 'win_id')
    op.drop_column('games', 'lose_id')
    # ### end Alembic commands ###
