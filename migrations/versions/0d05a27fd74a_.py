"""empty message

Revision ID: 0d05a27fd74a
Revises: 9f216b7a33fe
Create Date: 2020-12-18 08:26:30.665752

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0d05a27fd74a'
down_revision = '9f216b7a33fe'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TYPE fieldtype ADD VALUE 'choice'")
    op.execute("COMMIT")


def downgrade():
    op.execute("ALTER TYPE fieldtype REMOVE VALUE 'choice'")
    op.execute("COMMIT")
