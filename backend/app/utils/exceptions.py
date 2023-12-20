class ValidationException(Exception):
    """Class that defines a validation exception."""

    def __init__(self, message: str) -> None:
        self.message = message


class BussinesException(Exception):
    """Class that defines a business exception."""

    def __init__(self, message: str) -> None:
        self.message = message


class ForbiddenException(BussinesException):
    """Class that defines a forbidden exception."""

    def __init__(
        self,
        message: str = "You do not have permission to perform this action.",
    ) -> None:
        self.message = message


class NotFoundException(BussinesException):
    """Class that defines a not found exception."""

    def __init__(
        self, message: str = "The server can not find the requested resource."
    ) -> None:
        self.message = message


class AuthenticationInvalid:
    """Class that defines an invalid authentication exception."""

    def __init__(
        self, message: str = "The authentication key provided is invalid."
    ) -> None:
        self.message = message
