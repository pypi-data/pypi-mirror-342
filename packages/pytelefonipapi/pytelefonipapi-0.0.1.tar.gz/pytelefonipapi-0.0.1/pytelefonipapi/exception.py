class CustomException(Exception):
    pass


class TokenException(CustomException):
    """Primary exception for errors thrown in the get token post request."""

    def __init__(self, name_class, name_method, message):
        super().__init__(f"Class: \"{name_class}\", Method: \"{name_method}\", Message: {message}")


class SetSession(CustomException):
    """Base exception for errors caused within a get couriers."""

    def __init__(self, name_class, name_method, message):
        super().__init__(f"Class: \"{name_class}\", Method: \"{name_method}\", Message: {message}")

