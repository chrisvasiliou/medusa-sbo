"""empty message

Revision ID: 83df911f516c
Revises: 44bb979a8c3a
Create Date: 2017-11-27 15:20:23.580789

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83df911f516c'
down_revision = '44bb979a8c3a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('deliverable', sa.Column('secondary_location_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'deliverable', 'secondary_location', ['secondary_location_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'deliverable', type_='foreignkey')
    op.drop_column('deliverable', 'secondary_location_id')
    # ### end Alembic commands ###