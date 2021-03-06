"""empty message

Revision ID: 83d645d8e279
Revises: f45036e316fe
Create Date: 2019-12-03 17:40:55.740656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83d645d8e279'
down_revision = 'f45036e316fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('status', sa.String(), nullable=False))
    op.drop_column('games', 'confirmed')
    op.add_column('results', sa.Column('result_confirmed', sa.Boolean(), nullable=False))
    op.drop_column('results', 'confirmed')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('results', sa.Column('confirmed', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('results', 'result_confirmed')
    op.add_column('games', sa.Column('confirmed', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('games', 'status')
    # ### end Alembic commands ###
