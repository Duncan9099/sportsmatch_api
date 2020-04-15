"""empty message

Revision ID: 2c56b574c6ee
Revises: b8db39516b80
Create Date: 2020-03-03 18:25:26.336485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c56b574c6ee'
down_revision = 'b8db39516b80'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('players', 'last_name',
               existing_type=sa.VARCHAR(length=60),
               nullable=True)
    op.alter_column('players', 'postcode',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('players', 'postcode',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    op.alter_column('players', 'last_name',
               existing_type=sa.VARCHAR(length=60),
               nullable=False)
    # ### end Alembic commands ###