"""empty message

Revision ID: ae1b801eb125
Revises: 575509f11860
Create Date: 2020-10-16 01:21:52.564867

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae1b801eb125'
down_revision = '575509f11860'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('lead', 'amount')
    op.add_column('lead', sa.Column('amount', sa.FLOAT(), autoincrement=False, nullable=True))


def downgrade():
    op.drop_column('lead', 'amount')
    op.add_column('lead', sa.Column('amount', sa.INTEGER(), autoincrement=False, nullable=True))
