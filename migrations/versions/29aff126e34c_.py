"""empty message

Revision ID: 29aff126e34c
Revises: ae1b801eb125
Create Date: 2020-10-17 10:25:26.140512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29aff126e34c'
down_revision = 'ae1b801eb125'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('action',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('veokit_installation_id', sa.Integer(), nullable=False),
    sa.Column('lead_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('create_lead', 'update_lead', 'update_lead_status', 'archive_lead', 'restore_lead', name='actiontype'), nullable=False),
    sa.Column('old_status_id', sa.Integer(), nullable=True),
    sa.Column('new_status_id', sa.Integer(), nullable=True),
    sa.Column('log_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['lead_id'], ['lead.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['new_status_id'], ['status.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['old_status_id'], ['status.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_action_veokit_installation_id'), 'action', ['veokit_installation_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_action_veokit_installation_id'), table_name='action')
    op.drop_table('action')
    # ### end Alembic commands ###