"""Error message for the API"""


class BaseErrorMessage:
    """Base error message class."""

    status_code: int
    message: str

    def __init__(self, *args):
        self.message = self.message.format(*args)


class UnsupportedFileTypeError(BaseErrorMessage):
    status_code = 400
    message = "File type not supported."


class FileTooLargeError(BaseErrorMessage):
    status_code = 400
    message = "File size exceeds the maximum allowed size"


class FileExistsError(BaseErrorMessage):
    status_code = 400
    message = "File already exists"


class SessionNotFoundError(BaseErrorMessage):
    status_code = 404
    message = "Chat session not found"


class UserNotFoundError(BaseErrorMessage):
    status_code = 404
    message = "User not found"

