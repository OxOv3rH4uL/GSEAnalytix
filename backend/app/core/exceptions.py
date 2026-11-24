class GSEApplicationError(Exception):
    """
    Base level exception
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

class NotFoundError(GSEApplicationError):
    """
    Raised when a resource is not present/available
    """
    pass

class DatabaseError(GSEApplicationError):
    """
    Raised when there is an issue with database
    """
    pass

class ProjectNotFoundError(NotFoundError):
    """
    Raised when the project is not found
    """
    pass

class DeviceNotFoundError(NotFoundError):
    """
    Raised when the device is not found
    """
    pass
