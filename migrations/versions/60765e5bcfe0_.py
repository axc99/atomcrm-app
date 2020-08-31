"""empty message

Revision ID: 60765e5bcfe0
Revises: 2f3956c8c4b8
Create Date: 2020-08-28 21:30:24.405872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60765e5bcfe0'
down_revision = '2f3956c8c4b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('token', sa.Column('add_date', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('token', 'add_date')
    # ### end Alembic commands ###