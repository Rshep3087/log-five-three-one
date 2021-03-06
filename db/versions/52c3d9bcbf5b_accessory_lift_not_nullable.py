"""Accessory lift not nullable

Revision ID: 52c3d9bcbf5b
Revises: 04e8213f7094
Create Date: 2020-04-04 18:14:10.857888

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '52c3d9bcbf5b'
down_revision = '04e8213f7094'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('accessory_lifts', 'lift',
               existing_type=mysql.VARCHAR(length=60),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('accessory_lifts', 'lift',
               existing_type=mysql.VARCHAR(length=60),
               nullable=True)
    # ### end Alembic commands ###
