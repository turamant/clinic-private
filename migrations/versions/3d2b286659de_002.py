"""002

Revision ID: 3d2b286659de
Revises: 24f298ec1a02
Create Date: 2022-09-03 23:29:36.072357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d2b286659de'
down_revision = '24f298ec1a02'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'doctors_patients', ['data_appointment'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'doctors_patients', type_='unique')
    # ### end Alembic commands ###