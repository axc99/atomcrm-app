"""empty message

Revision ID: 3a96d0ed82f4
Revises: b4f80ff8bfe1
Create Date: 2020-10-17 11:15:39.194981

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3a96d0ed82f4'
down_revision = 'b4f80ff8bfe1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lead_action',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('create_lead', 'update_lead', 'update_lead_status', 'archive_lead', 'restore_lead', name='leadactiontype'), nullable=False),
    sa.Column('old_status_id', sa.Integer(), nullable=True),
    sa.Column('new_status_id', sa.Integer(), nullable=True),
    sa.Column('log_date', sa.DateTime(), nullable=False),
    sa.Column('veokit_user_id', sa.Integer(), nullable=False),
    sa.Column('lead_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['lead_id'], ['lead.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['new_status_id'], ['status.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['old_status_id'], ['status.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lead_action_veokit_user_id'), 'lead_action', ['veokit_user_id'], unique=False)
    op.drop_index('ix_action_veokit_installation_id', table_name='action')
    op.drop_index('ix_action_veokit_user_id', table_name='action')
    op.drop_table('action')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('action',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('veokit_installation_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('lead_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('type', postgresql.ENUM('create_lead', 'update_lead', 'update_lead_status', 'archive_lead', 'restore_lead', name='actiontype'), autoincrement=False, nullable=False),
    sa.Column('old_status_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('new_status_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('log_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('veokit_user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['lead_id'], ['lead.id'], name='action_lead_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['new_status_id'], ['status.id'], name='action_new_status_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['old_status_id'], ['status.id'], name='action_old_status_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='action_pkey')
    )
    op.create_index('ix_action_veokit_user_id', 'action', ['veokit_user_id'], unique=False)
    op.create_index('ix_action_veokit_installation_id', 'action', ['veokit_installation_id'], unique=False)
    op.drop_index(op.f('ix_lead_action_veokit_user_id'), table_name='lead_action')
    op.drop_table('lead_action')
    # ### end Alembic commands ###