from ..common.failures import Failure


class Failures(object):

    empty_password = Failure({
        "error_category": "request_data",
        "error_type": "information_missing",
        "message": "Password cannot be empty",
        "details": None
    })

    passwords_doesnt_match = Failure({
        "error_category": "request_data",
        "error_type": "invalid_password",
        "message": "Passwords doesn't mach",
        "details": None
    })

    passwords_too_week = Failure({
        "error_category": "request_data",
        "error_type": "invalid_password",
        "message": "Password should attend the follow requirements:"
                   "- Be at least 8 characters long"
                   "- Have at least 1 uppercase letter"
                   "- Have at least 1 lowercase letter"
                   "- Have at least 1 special character",
        "details": None
    })

    username_already_exists = Failure({
        "error_category": "request_data",
        "error_type": "constraint_violation",
        "message": "username already being used by other user",
        "details": "the username of your choice is already being used by another user"
    })

    email_already_registered = Failure({
        "error_category": "request_data",
        "error_type": "constraint_violation",
        "message": "user already registered",
        "details": "Sorry, but looks like we already have an account registered for this email address"
    })
