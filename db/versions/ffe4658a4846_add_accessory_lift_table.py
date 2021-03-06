"""Add accessory lift table

Revision ID: ffe4658a4846
Revises: aaf838bdb0d8
Create Date: 2020-03-31 13:16:24.723832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffe4658a4846'
down_revision = 'aaf838bdb0d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accessory_lifts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lift', sa.String(length=60), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('accessory_lifts')
    # ### end Alembic commands ###
