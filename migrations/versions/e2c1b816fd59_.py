"""empty message

Revision ID: e2c1b816fd59
Revises: 9aeff7ffe1e4
Create Date: 2018-08-16 16:30:56.624547

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2c1b816fd59'
down_revision = '9aeff7ffe1e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('GuestInfo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('calendar_id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=30), nullable=True),
    sa.Column('phone_number', sa.String(length=30), nullable=True),
    sa.Column('guests', sa.Integer(), nullable=True),
    sa.Column('nights', sa.Integer(), nullable=True),
    sa.Column('total_cost', sa.Integer(), nullable=True),
    sa.Column('currency', sa.String(length=30), nullable=True),
    sa.Column('from_time', sa.String(length=30), nullable=True),
    sa.Column('to_time', sa.String(length=30), nullable=True),
    sa.ForeignKeyConstraint(['calendar_id'], ['Property.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('Renter')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Renter',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Renter_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('property_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('system_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_name', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('phone_number', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('guests', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('from_date', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('to_date', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('from_time', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('to_time', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('currency', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('nights', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('total_cost', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['property_id'], ['Property.id'], name='Renter_property_id_fkey'),
    sa.ForeignKeyConstraint(['system_id'], ['Dir_system.id'], name='Renter_system_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Renter_pkey')
    )
    op.drop_table('GuestInfo')
    # ### end Alembic commands ###
