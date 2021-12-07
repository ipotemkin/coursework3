class NotFoundError(Exception):
    pass


class BadRequestError(Exception):
    pass


class ValidationError(Exception):
    pass


class NoContentError(Exception):
    pass


class DatabaseError(Exception):
    pass
