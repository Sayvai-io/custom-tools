"""Exception Classes for Sayvai Tools"""

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


