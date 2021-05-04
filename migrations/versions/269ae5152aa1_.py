"""empty message

Revision ID: 269ae5152aa1
Revises: cfb890285269
Create Date: 2021-04-18 15:25:38.965072

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '269ae5152aa1'
down_revision = 'cfb890285269'
branch_labels = None
depends_on = None


def upgrade():
    # Rename installation_card_settings to installation_settings
    conn = op.get_bind()
    conn.execute("""ALTER TABLE installation_card_settings RENAME TO installation_settings;""")
    conn.execute("""ALTER INDEX ix_installation_card_settings_nepkit_installation_id RENAME TO ix_installation_settings_nepkit_installation_id;""")

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('installation_settings', sa.Column('notifications_new_lead_api_enabled', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('installation_settings', sa.Column('notifications_new_lead_extension_enabled', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('installation_settings', sa.Column('notifications_new_lead_user_enabled', sa.Boolean(), nullable=False, server_default='FALSE'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('installation_settings', 'notifications_new_lead_user_enabled')
    op.drop_column('installation_settings', 'notifications_new_lead_extension_enabled')
    op.drop_column('installation_settings', 'notifications_new_lead_api_enabled')
    op.create_table('installation_card_settings',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('amount_enabled', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('currency', postgresql.ENUM('usd', 'cad', 'eur', 'aed', 'afn', 'all', 'amd', 'ars', 'aud', 'azn', 'bam', 'bdt', 'bgn', 'bhd', 'bif', 'bnd', 'bob', 'brl', 'bwp', 'byn', 'bzd', 'cdf', 'chf', 'clp', 'cny', 'cop', 'crc', 'cve', 'czk', 'djf', 'dkk', 'dop', 'dzd', 'eek', 'egp', 'ern', 'etb', 'gbp', 'gel', 'ghs', 'gnf', 'gtq', 'hkd', 'hnl', 'hrk', 'huf', 'idr', 'ils', 'inr', 'iqd', 'irr', 'isk', 'jmd', 'jod', 'jpy', 'kes', 'khr', 'kmf', 'krw', 'kwd', 'kzt', 'lbp', 'lkr', 'ltl', 'lvl', 'lyd', 'mad', 'mdl', 'mga', 'mkd', 'mmk', 'mop', 'mur', 'mxn', 'myr', 'mzn', 'nad', 'ngn', 'nio', 'nok', 'npr', 'nzd', 'omr', 'pab', 'pen', 'php', 'pkr', 'pln', 'pyg', 'qar', 'ron', 'rsd', 'rub', 'rwf', 'sar', 'sdg', 'sek', 'sgd', 'sos', 'syp', 'thb', 'tnd', 'top', 'tru', 'ttd', 'twd', 'tzs', 'uah', 'ugx', 'uyu', 'uzs', 'vef', 'vnd', 'xaf', 'xof', 'yer', 'zar', 'zmk', 'zwl', name='cardcurrencies'), autoincrement=False, nullable=False),
    sa.Column('nepkit_installation_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='installation_card_settings_pkey')
    )
    op.create_index('ix_installation_card_settings_nepkit_installation_id', 'installation_card_settings', ['nepkit_installation_id'], unique=False)
    # ### end Alembic commands ###