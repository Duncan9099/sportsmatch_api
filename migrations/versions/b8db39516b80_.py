"""empty message

Revision ID: b8db39516b80
Revises: 4c0673b2bf05
Create Date: 2020-02-27 17:41:29.964108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8db39516b80'
down_revision = '4c0673b2bf05'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('players', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('players', sa.Column('longitude', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('players', 'longitude')
    op.drop_column('players', 'latitude')
    # ### end Alembic commands ###
