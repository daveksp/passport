from flask_security.utils import encrypt_password
from werkzeug.security import gen_salt

from ..models import User, Client, Grant, Role, Token, roles_users


DB_MODELS = [User, Client, Grant, Token, roles_users]


def recreate_db(db, bind='__all__', app=None):
    """
    Drop existing tables and create new ones according to the current schema.
    """
    db.drop_all(bind=bind, app=app)
    db.create_all(bind=bind, app=app)
    roles = create_roles(db)
    admin_user = create_admin_user(db, roles[0])
    create_clients(db, admin_user)


def create_tables(db, bind='__all__', app=None):
    """
    Create all missing tables according to the current schema.
    """
    db.create_all(bind=bind, app=app)
    roles = create_roles(db)
    admin_user = create_admin_user(db, roles[0])
    create_clients(db, admin_user)


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

    return roles


def create_admin_user(db, admin_role):
    user = User(username='admin', email='dkspinheiro@gmail.com', 
                password=encrypt_password('123456'), roles=[admin_role])

    db.session.add(user)
    db.session.commit()
    return user


def create_clients(db, user):
    clients = [
        {'name': 'stats', 'description': 'api for generating statistics'},
        {'name': 'inventory', 'description': 'api for mananging inventory'},
        {'name': 'payment', 'description': 'api for mananging payment options'},
        {'name': 'transactions', 'description': 'api for mananging transactions between users/teams'},
        {'name': 'campaigns', 'description': 'api for mananging team campaings'},
    ]
    for client in clients:
        client_obj = Client(
            name=client['name'],
            description=client['description'],
            client_id=gen_salt(40),
            client_secret=gen_salt(50),
            _redirect_uris=None,
            _default_scopes='email',
            user_id=user.id,
        )
        db.session.add(client_obj)
    db.session.commit()
