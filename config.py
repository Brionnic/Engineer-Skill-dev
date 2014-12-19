__author__ = 'brharden'

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'as_skills.db')
WHOOSH_BASE = os.path.join(basedir, 'new_search.db')

print 'SQLALCHEMY_DATABASE_URI is: ', SQLALCHEMY_DATABASE_URI

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True