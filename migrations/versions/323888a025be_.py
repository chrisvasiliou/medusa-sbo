"""empty message

Revision ID: 323888a025be
Revises: e5051545a293
Create Date: 2017-11-26 16:45:58.092842

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '323888a025be'
down_revision = 'e5051545a293'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Deliverable_ITC_map', 'comments',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('ITC', 'description',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('ITP', 'description',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('location', 'secondary_location',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('location', 'secondary_location',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('ITP', 'description',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('ITC', 'description',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('Deliverable_ITC_map', 'comments',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###