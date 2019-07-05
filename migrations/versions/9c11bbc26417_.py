"""empty message

Revision ID: 9c11bbc26417
Revises: 6bf7fe39c0d1
Create Date: 2018-07-31 15:37:10.689518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c11bbc26417'
down_revision = '6bf7fe39c0d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Calendar',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('property_id', sa.Integer(), nullable=False),
    sa.Column('availability', sa.String(length=30), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('currency', sa.String(length=30), nullable=True),
    sa.Column('date', sa.String(length=30), nullable=True),
    sa.ForeignKeyConstraint(['property_id'], ['Property.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Calendar')
    # ### end Alembic commands ###
