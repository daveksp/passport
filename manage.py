#!/usr/bin/env python
from flask_migrate import MigrateCommand
from flask_script import Manager

from passport import create_app
from passport.manage import RebuildDbCommand, CreateTablesCommand


manager = Manager(create_app)
manager.add_command('rebuilddb', RebuildDbCommand())
manager.add_command('create_tables', CreateTablesCommand())
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
