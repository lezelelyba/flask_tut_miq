#!flask/bin/python

import migrate.versioning

from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

migrate.versioning.upgrade(
        SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = migrate.versioning.db_version(
        SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('Current dtabase version ' + str(v))
