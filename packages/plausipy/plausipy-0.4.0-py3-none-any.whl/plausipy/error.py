class PlausipyError(Exception):
    """Base class for all exceptions raised by Plausipy."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
