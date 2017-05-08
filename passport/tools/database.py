from ..models import User, Client, Grant, Role, Token


DB_MODELS = [User, Client, Grant, Token]


def recreate_db(db, bind='__all__', app=None):
    """
    Drop existing tables and create new ones according to the current schema.
    """
    db.drop_all(bind=bind, app=app)
    db.create_all(bind=bind, app=app)
    create_roles(db)


def create_tables(db, bind='__all__', app=None):
    """
    Create all missing tables according to the current schema.
    """
    db.create_all(bind=bind, app=app)
    create_roles(db)


def create_roles(db):
    roles = [
        Role(id=1, name='admin', description='admin role'),
        Role(id=2, name='agent', description='agent role'),
        Role(id=3, name='club', description='club role'),
        Role(id=4, name='supporter', description='supporter role')
    ]

    for role in roles:
        db.session.add(role)

    db.session.commit()
