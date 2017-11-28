from ..common.failures import Failure


class Failures(object):

    client_name_already_exists = Failure({
        "error_category": "request_data",
        "error_type": "constraint_violation",
        "message": "client name already registered",
        "details": "the client name of your choice is already being used by another api"
    })
