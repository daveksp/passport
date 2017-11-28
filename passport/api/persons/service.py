from ...extensions import db
from ...models import Person

from .schema import PersonSchema


schema = PersonSchema()


def person_schema_load(json):
    schema = PersonSchema()
    return schema.load(json or {})[0]


def person_schema_dump(person):
    return schema.dump(person)[0]


def save_and_dump_person(person):
    db.session.add(person)
    db.session.commit()

    return person_schema_dump(person)
