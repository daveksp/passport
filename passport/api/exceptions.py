class ApiException(Exception):
    def __init__(self, errors=[], *args, **kwargs):
        super(ApiException, self).__init__(*args, **kwargs)
        self.errors = errors


class RequestDataException(ApiException):
    def __init__(self, errors=[], *args, **kwargs):
        super(RequestDataException, self).__init__(*args, **kwargs)
        self.errors = errors


class AccountException(ApiException):
    def __init__(self, errors=[], *args, **kwargs):
        super(AccountException, self).__init__(*args, **kwargs)
        self.errors = errors
