#!flask/bin/python

import migrate.versioning
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

v = migrate.versioning.api.db_version(
        SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
migrate.versioning.api.downgrade(
        SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)

v = migrate.versioning.api.db_version(
        SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('Current dtabase version ' + str(v))
