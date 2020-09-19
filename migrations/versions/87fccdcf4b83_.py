"""empty message

Revision ID: 87fccdcf4b83
Revises: 2db6b9a1fd5d
Create Date: 2020-09-06 12:20:22.213140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from flaskr import db
from flaskr.models.field import Field
from flaskr.models.lead import Lead
from flaskr.models.status import Status
from flaskr.models.tag import Tag
from flaskr.models.token import Token

revision = '87fccdcf4b83'
down_revision = '2db6b9a1fd5d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('field', sa.Column('veokit_installation_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_field_veokit_installation_id'), 'field', ['veokit_installation_id'], unique=False)
    op.drop_index('ix_field_veokit_system_id', table_name='field')
    op.drop_column('field', 'veokit_system_id')

    op.add_column('lead', sa.Column('veokit_installation_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_lead_veokit_installation_id'), 'lead', ['veokit_installation_id'], unique=False)
    op.drop_index('ix_lead_veokit_system_id', table_name='lead')
    op.drop_column('lead', 'veokit_system_id')

    op.add_column('status', sa.Column('veokit_installation_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_status_veokit_installation_id'), 'status', ['veokit_installation_id'], unique=False)
    op.drop_index('ix_status_veokit_system_id', table_name='status')
    op.drop_column('status', 'veokit_system_id')

    op.add_column('tag', sa.Column('veokit_installation_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_tag_veokit_installation_id'), 'tag', ['veokit_installation_id'], unique=False)
    op.drop_index('ix_tag_veokit_system_id', table_name='tag')
    op.drop_column('tag', 'veokit_system_id')

    op.add_column('token', sa.Column('veokit_installation_id', sa.Integer(), nullable=True))
    op.drop_column('token', 'veokit_system_id')


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('token', sa.Column('veokit_system_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('token', 'veokit_installation_id')
    op.add_column('tag', sa.Column('veokit_system_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_index('ix_tag_veokit_system_id', 'tag', ['veokit_system_id'], unique=False)
    op.drop_index(op.f('ix_tag_veokit_installation_id'), table_name='tag')
    op.drop_column('tag', 'veokit_installation_id')
    op.add_column('status', sa.Column('veokit_system_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_index('ix_status_veokit_system_id', 'status', ['veokit_system_id'], unique=False)
    op.drop_index(op.f('ix_status_veokit_installation_id'), table_name='status')
    op.drop_column('status', 'veokit_installation_id')
    op.add_column('lead', sa.Column('veokit_system_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_index('ix_lead_veokit_system_id', 'lead', ['veokit_system_id'], unique=False)
    op.drop_index(op.f('ix_lead_veokit_installation_id'), table_name='lead')
    op.drop_column('lead', 'veokit_installation_id')
    op.add_column('field', sa.Column('veokit_system_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_index('ix_field_veokit_system_id', 'field', ['veokit_system_id'], unique=False)
    op.drop_index(op.f('ix_field_veokit_installation_id'), table_name='field')
    op.drop_column('field', 'veokit_installation_id')
    # ### end Alembic commands ###
