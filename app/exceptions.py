class AppError(Exception):
    """Base class for app errors."""

    pass


class RiotAPIError(AppError):
    pass


class PlayerNotFoundError(AppError):
    pass
