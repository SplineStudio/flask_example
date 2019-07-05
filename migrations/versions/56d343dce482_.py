"""empty message

Revision ID: 56d343dce482
Revises: 3cae3295d6d7
Create Date: 2018-08-10 10:30:06.057703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56d343dce482'
down_revision = '3cae3295d6d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Renter', 'bool_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Renter', sa.Column('bool_time', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
