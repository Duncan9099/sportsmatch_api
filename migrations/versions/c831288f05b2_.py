"""empty message

Revision ID: c831288f05b2
Revises: d1e1d1f1e687
Create Date: 2020-05-30 12:11:28.719195

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'c831288f05b2'
down_revision = 'd1e1d1f1e687'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('players', 'sport')
    op.drop_column('players', 'rank_points')
    op.drop_column('players', 'ability')
    op.alter_column('players', 'profile_image',
               existing_type=postgresql.BYTEA(),
               type_=sa.String(length=128),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('players', sa.Column('ability', sa.String(length=50), autoincrement=False, nullable=True))
    op.add_column('players', sa.Column('rank_points', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('players', sa.Column('sport', sa.String(length=30), autoincrement=False, nullable=True))
    op.alter_column('players', 'profile_image',
               existing_type=postgresql.BYTEA(),
               nullable=True)
    # ### end Alembic commands ###
