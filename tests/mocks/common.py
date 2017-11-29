from datetime import datetime


def user_data(json=False):
    return {
        "id": 1,
        "username": "test username",
        "email": "test@email.com",
        "password": "Abcdeg9#a",
        "retype_password": "Abcdeg9#a",
        "active": 'true' if json else True,
        "confirmed_at": str(datetime.now()) if json else datetime.now(),
        "roles": [],
        "person": person_data()}

def person_data(json=False):
    return{
        "first_name": "Test",
        "last_name": "Surname"
    }

def role_data(json=False):
    return{
        "name": "Test Role",
        "description": "test description"
    }

def client_data(json=False):
    return{
        "name": "Test Client",
        "description": "test description",
        "redirect_uris": "['http://localhost:5000']"
    }
