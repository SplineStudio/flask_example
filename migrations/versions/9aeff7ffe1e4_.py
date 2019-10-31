"""empty message

Revision ID: 9aeff7ffe1e4
Revises: d61bc289fe9e
Create Date: 2018-08-16 16:04:33.435584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9aeff7ffe1e4'
down_revision = 'd61bc289fe9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Renter', 'system_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Renter', 'system_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###