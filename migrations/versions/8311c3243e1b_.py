"""empty message

Revision ID: 8311c3243e1b
Revises: 83d645d8e279
Create Date: 2020-01-11 11:24:41.286714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8311c3243e1b'
down_revision = '83d645d8e279'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('receiver_id', sa.Integer(), nullable=False))
    op.drop_constraint('messages_game_id_fkey', 'messages', type_='foreignkey')
    op.drop_constraint('messages_opponent_id_fkey', 'messages', type_='foreignkey')
    op.drop_constraint('messages_organiser_id_fkey', 'messages', type_='foreignkey')
    op.create_foreign_key(None, 'messages', 'players', ['receiver_id'], ['id'])
    op.drop_column('messages', 'game_id')
    op.drop_column('messages', 'opponent_id')
    op.drop_column('messages', 'organiser_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('organiser_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('messages', sa.Column('opponent_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('messages', sa.Column('game_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'messages', type_='foreignkey')
    op.create_foreign_key('messages_organiser_id_fkey', 'messages', 'players', ['organiser_id'], ['id'])
    op.create_foreign_key('messages_opponent_id_fkey', 'messages', 'players', ['opponent_id'], ['id'])
    op.create_foreign_key('messages_game_id_fkey', 'messages', 'games', ['game_id'], ['id'])
    op.drop_column('messages', 'receiver_id')
    # ### end Alembic commands ###
