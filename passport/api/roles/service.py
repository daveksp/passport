from ...models import Role


def list_roles(role_id=None):
    query = Role.query
    query = query.filter_by(id=role_id) if role_id else query
    return query.all()