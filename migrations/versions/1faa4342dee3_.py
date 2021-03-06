"""empty message

Revision ID: 1faa4342dee3
Revises: 3e3a74e0dd36
Create Date: 2020-02-02 11:23:06.948597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1faa4342dee3'
down_revision = '3e3a74e0dd36'
branch_labels = None
depends_on = None


def upgrade():
    ### actual upgrade
    op.add_column('messages', sa.Column('receiver_read', sa.Boolean(), nullable=False))
    op.add_column('messages', sa.Column('sender_read', sa.Boolean(), nullable=False))
    op.drop_column('messages', 'read')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('read', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('messages', 'sender_read')
    op.drop_column('messages', 'receiver_read')
    # ### end Alembic commands ###
