from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('engineer', String(length=100)),
    Column('engineer_name_first', String(length=26)),
    Column('engineer_name_last', String(length=40)),
    Column('message', String(length=255)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['engineer_name_first'].create()
    post_meta.tables['user'].columns['engineer_name_last'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['engineer_name_first'].drop()
    post_meta.tables['user'].columns['engineer_name_last'].drop()
