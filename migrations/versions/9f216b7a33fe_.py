"""empty message

Revision ID: 9f216b7a33fe
Revises: a66e6480f3cf
Create Date: 2020-12-18 07:55:35.386519

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9f216b7a33fe'
down_revision = 'a66e6480f3cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('field', sa.Column('choice_options', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('field', 'choice_options')
    # ### end Alembic commands ###
