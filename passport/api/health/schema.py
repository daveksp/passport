from ..extensions import schemas


class HealthSchema(schemas.Schema):

    health = schemas.String()
