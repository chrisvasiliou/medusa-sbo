"""empty message

Revision ID: 5251436c54d0
Revises: ff9c214dc46e
Create Date: 2017-05-31 16:41:55.676946

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5251436c54d0'
down_revision = 'ff9c214dc46e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alarm',
    sa.Column('Medusa_ID', sa.Integer(), nullable=False),
    sa.Column('site_id', sa.Integer(), nullable=False),
    sa.Column('SeqNo', sa.BigInteger(), nullable=True),
    sa.Column('MonitoredPoint', sa.String(length=1024), nullable=True),
    sa.Column('PreviousAlarmState', sa.Integer(), nullable=True),
    sa.Column('AlarmState', sa.Integer(), nullable=True),
    sa.Column('TriggeredTimestamp', sa.DateTime(), nullable=True),
    sa.Column('AdvancedEvaluationState', sa.Integer(), nullable=True),
    sa.Column('AlarmType', sa.String(length=1024), nullable=True),
    sa.Column('MonitoredValue', sa.String(length=50), nullable=True),
    sa.Column('DomainName', sa.String(length=1024), nullable=True),
    sa.Column('AcknowledgedBy', sa.String(length=80), nullable=True),
    sa.Column('Priority', sa.Integer(), nullable=True),
    sa.Column('Count', sa.Integer(), nullable=True),
    sa.Column('AcknowledgeTime', sa.DateTime(), nullable=True),
    sa.Column('BasicEvaluationState', sa.Boolean(), nullable=True),
    sa.Column('Logging', sa.Boolean(), nullable=True),
    sa.Column('Hidden', sa.Boolean(), nullable=True),
    sa.Column('Category', sa.String(length=128), nullable=True),
    sa.Column('AssignedTo', sa.String(length=80), nullable=True),
    sa.Column('AssignState', sa.Integer(), nullable=True),
    sa.Column('DisabledBy', sa.Integer(), nullable=True),
    sa.Column('AlarmStateSeqNo', sa.BigInteger(), nullable=True),
    sa.Column('CheckedSteps', sa.String(length=512), nullable=True),
    sa.Column('AudibleAlert', sa.Boolean(), nullable=True),
    sa.Column('FlashingAlert', sa.Boolean(), nullable=True),
    sa.Column('Silence', sa.Boolean(), nullable=True),
    sa.Column('PendingState', sa.Integer(), nullable=True),
    sa.Column('PendingCommand', sa.Integer(), nullable=True),
    sa.Column('ServerOffline', sa.Boolean(), nullable=True),
    sa.Column('SystemEventId', sa.BigInteger(), nullable=True),
    sa.Column('Module', sa.Integer(), nullable=True),
    sa.Column('HasAttachment', sa.Boolean(), nullable=True),
    sa.Column('UniqueAlarmId', sa.String(length=50), nullable=True),
    sa.Column('SystemAlarmId', sa.Integer(), nullable=True),
    sa.Column('AlarmText', sa.String(length=1024), nullable=True),
    sa.Column('Command', sa.String(length=128), nullable=True),
    sa.Column('OriginatedGUID', sa.String(length=50), nullable=True),
    sa.Column('DateTimeStamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['site_id'], ['site.ID'], ),
    sa.PrimaryKeyConstraint('Medusa_ID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('alarm')
    # ### end Alembic commands ###
