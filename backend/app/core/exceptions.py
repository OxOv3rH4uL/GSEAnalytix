class GSEApplicationError(Exception):
    """
    Base level exception
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class FoundError(GSEApplicationError):
    """
    Raised when a resource is already present/available
    """

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

class ProjectFoundError(FoundError):
    """
    Raised when the project is already present
    """
    pass

class DeviceFoundError(FoundError):
    """
    Raised when a device is already present
    """
    pass


