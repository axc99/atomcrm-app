"""empty message

Revision ID: e54b35c174d0
Revises: 0d05a27fd74a
Create Date: 2020-12-20 15:01:09.136423

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e54b35c174d0'
down_revision = '0d05a27fd74a'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TYPE fieldtype ADD VALUE 'phone'")
    op.execute("ALTER TYPE fieldtype ADD VALUE 'email'")
    op.execute("COMMIT")


def downgrade():
    op.execute("ALTER TYPE fieldtype REMOVE VALUE 'phone'")
    op.execute("ALTER TYPE fieldtype REMOVE VALUE 'email'")
    op.execute("COMMIT")
