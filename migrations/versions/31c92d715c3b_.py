"""empty message

Revision ID: 31c92d715c3b
Revises: 
Create Date: 2017-04-26 09:51:41.648683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31c92d715c3b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tbLogTimeValues',
    sa.Column('DateTimeStamp', sa.DateTime(), nullable=True),
    sa.Column('SeqNo', sa.BigInteger(), nullable=False),
    sa.Column('FloatVALUE', sa.Float(), nullable=True),
    sa.Column('ParentID', sa.Integer(), nullable=False),
    sa.Column('OdometerValue', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('SeqNo', 'ParentID')
    )
    op.create_table('tbLoggedEntities',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('GUID', sa.String(length=50), nullable=True),
    sa.Column('Path', sa.String(length=1024), nullable=True),
    sa.Column('Descr', sa.String(length=512), nullable=True),
    sa.Column('Disabled', sa.Boolean(), nullable=True),
    sa.Column('LastMod', sa.DateTime(), nullable=True),
    sa.Column('Version', sa.Integer(), nullable=True),
    sa.Column('Type', sa.String(length=80), nullable=True),
    sa.Column('LogPoint', sa.String(length=1024), nullable=True),
    sa.Column('UNITPREFIX', sa.String(length=512), nullable=True),
    sa.Column('Unit', sa.String(length=512), nullable=True),
    sa.Column('BaseValue', sa.Float(), nullable=True),
    sa.Column('MeterStartPoint', sa.Float(), nullable=True),
    sa.Column('LastReadValue', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('ID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tbLoggedEntities')
    op.drop_table('tbLogTimeValues')
    # ### end Alembic commands ###
