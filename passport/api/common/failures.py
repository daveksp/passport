from copy import copy


class Failure(object):

    def __init__(self, initval=None):
        self.val = initval

    def __get__(self, obj, objtype):
        return copy(self.val)

    def __set__(self, obj, val):
        self.val = val


class Failures(object):

    information_missing = Failure({
        "error_category": "request_data",
        "error_type": "information_missing",
        "message": "One or more required fields were omitted from the request.",
        "details": None
    })

    other_error = Failure({
        "error_category": "general",
        "error_type": "other",
        "message": "Other error (contact BPTechnologies for support).",
        "details": None
    })
