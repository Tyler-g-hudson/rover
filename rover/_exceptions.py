class HashCollisionError(Exception):
    """Raised when a repo file has a different hash than its known hash."""

    def __init__(self, message: str = ""):
        super().__init__(message)
