"""empty message

Revision ID: 0bf55fa82fa2
Revises: 8866957e4add
Create Date: 2020-10-22 20:39:22.992177

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0bf55fa82fa2'
down_revision = '8866957e4add'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('installation_integration_settings', 'integration')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('installation_integration_settings', sa.Column('integration', postgresql.ENUM('tilda', name='installationintegration'), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
