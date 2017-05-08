from flask_script import Command

from .extensions import db
from .tools.database import recreate_db, create_tables


class RebuildDbCommand(Command):
    """Rebuild the database"""

    def run(self):
        recreate_db(db)


class CreateTablesCommand(Command):
    """Create missing tables"""

    def run(self):
        create_tables(db)
