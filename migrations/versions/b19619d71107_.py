"""empty message

Revision ID: b19619d71107
Revises: dc14cb33db11
Create Date: 2018-08-03 11:25:38.721771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b19619d71107'
down_revision = 'dc14cb33db11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Calendar', sa.Column('end_date', sa.String(length=30), nullable=True))
    op.add_column('Calendar', sa.Column('start_date', sa.String(length=30), nullable=True))
    op.drop_column('Calendar', 'date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Calendar', sa.Column('date', sa.VARCHAR(length=30), autoincrement=False, nullable=True))
    op.drop_column('Calendar', 'start_date')
    op.drop_column('Calendar', 'end_date')
    # ### end Alembic commands ###
