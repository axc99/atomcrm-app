"""empty message

Revision ID: 4839b9f618e3
Revises: 41bd3cbe72da
Create Date: 2020-11-05 00:39:30.837839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4839b9f618e3'
down_revision = '41bd3cbe72da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('field', 'name',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=40),
               existing_nullable=False)
    op.alter_column('status', 'name',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=30),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('status', 'name',
               existing_type=sa.String(length=30),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
    op.alter_column('field', 'name',
               existing_type=sa.String(length=40),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
    # ### end Alembic commands ###