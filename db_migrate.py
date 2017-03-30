#!flask/bin/python

import imp
import migrate.versioning
import app

from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

v = migrate.versioning.db_version(
        SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))

tmp_module = imp.new_module('old_model')
old_model = migrate.versioning.create_model(
        SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

exec(old_model, tmp_module.__dict__)

script = migrate.versioning.make_update_script_for_model(
        SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_MIGRATE_REPO,
        tmp_module.meta, app.db.metadata)

open(migration, "wt").write(script)

migrate.versioning.upgrade(
        SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = migrate.versioning.db_version(
        SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

print('New migration saved as ' + migration)
print('Current database version: ' + str(v))
