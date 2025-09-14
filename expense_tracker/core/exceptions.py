"""
This module defines custom exceptions used throughout the application for specific error conditions.
"""

class AppException(Exception):
    """
    Base class for all application-specific exceptions.
    """
    pass

class AuthenticationError(AppException):
    """
    Raised for failed login attempts.
    """
    pass

class UserExistsError(AppException):
    """
    Raised when trying to register a user that already exists.
    """
    pass

class ValidationError(AppException):
    """
    Raised when user input fails validation checks.
    """
    pass

class ResourceNotFoundError(AppException):
    """
    Raised when a database resource (e.g., an account) is not found.
    """
    pass