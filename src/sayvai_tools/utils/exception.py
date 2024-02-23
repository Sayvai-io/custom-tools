"""Exception Classes for Sayvai Tools"""

import functools
import warnings


class SayvaiToolsError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class SayvaiToolsWarning(Warning):
    """Base class for warnings in this module."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class SayvaiToolsDeprecatedWarning(DeprecationWarning):
    """Base class for deprecated warnings in this module."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


def deprecated(
    message="This class is deprecated and will be removed in future versions.",
):
    """
    Decorator to mark a class as deprecated.
    """

    def decorator(cls):
        @functools.wraps(cls)
        def wrapper(*args, **kwargs):
            warnings.warn(message, SayvaiToolsDeprecatedWarning, stacklevel=2)
            return cls(*args, **kwargs)

        return wrapper

    return decorator
