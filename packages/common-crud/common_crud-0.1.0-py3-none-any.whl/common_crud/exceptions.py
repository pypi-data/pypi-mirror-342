from typing import Optional


class CRUDError(Exception):
    """Basic exception for CRUD operation errors."""
    def __init__(self, message: str, cause: Optional[Exception] = None):
        self.message = message
        self.cause = cause
        super().__init__(message)


class ModelNotSetError(CRUDError):
    """Exception when the model is not installed."""
    pass


class InvalidFilterError(CRUDError):
    """Exception for invalid filters."""
    pass


class DatabaseError(CRUDError):
    """Exception for database errors."""
    pass
