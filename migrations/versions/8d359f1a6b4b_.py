"""empty message

Revision ID: 8d359f1a6b4b
Revises: 915f8dff4f7d
Create Date: 2017-09-19 15:30:41.146077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d359f1a6b4b'
down_revision = '915f8dff4f7d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'Check_generic', ['check_description'])
    op.create_unique_constraint(None, 'ITC', ['name'])
    op.create_unique_constraint('_project_name_uc', 'ITP', ['project_id', 'name'])
    op.drop_index('name', table_name='ITP')
    op.create_unique_constraint('_ITP_name_uc', 'deliverable', ['ITP_id', 'name'])
    op.drop_index('name', table_name='project')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('name', 'project', ['name'], unique=True)
    op.drop_constraint('_ITP_name_uc', 'deliverable', type_='unique')
    op.create_index('name', 'ITP', ['name'], unique=True)
    op.drop_constraint('_project_name_uc', 'ITP', type_='unique')
    op.drop_constraint(None, 'ITC', type_='unique')
    op.drop_constraint(None, 'Check_generic', type_='unique')
    # ### end Alembic commands ###
