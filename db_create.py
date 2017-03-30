#!flask/bin/python

import os.path

import migrate.versioning
import app

from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

app.db.create_all()

if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    migrate.versioning.api.create(
            SQLALCHEMY_MIGRATE_REPO, 'database repository')
    migrate.versioning.api.version_control(
            SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    migrate.versioning.api.version_control(
            SQLALCHEMY_DATABASE_URI,
            SQLALCHEMY_MIGRATE_REPO,
            migrate.versioning.api.version(SQLALCHEMY_MIGRATE_REPO))
