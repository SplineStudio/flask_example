"""empty message

Revision ID: 962ffa0773d0
Revises: e2c1b816fd59
Create Date: 2018-08-16 18:33:30.040063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '962ffa0773d0'
down_revision = 'e2c1b816fd59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('GuestInfo_calendar_id_fkey', 'GuestInfo', type_='foreignkey')
    op.create_foreign_key(None, 'GuestInfo', 'Calendar', ['calendar_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'GuestInfo', type_='foreignkey')
    op.create_foreign_key('GuestInfo_calendar_id_fkey', 'GuestInfo', 'Property', ['calendar_id'], ['id'])
    # ### end Alembic commands ###
