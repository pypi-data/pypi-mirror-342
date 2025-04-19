"""Package exceptions."""

from click import UsageError


class PackageBaseException(Exception):

    """A base exception for isabl_cli."""


class ValidationError(PackageBaseException, UsageError, AssertionError):

    """A class to raise when a validation error occurs."""


class MissingRequirementError(PackageBaseException):

    """A class to raise when a requirement is missing."""


class MissingOutputError(PackageBaseException):

    """A class to raise when a file that should exist is missing."""


class ConfigurationError(PackageBaseException):

    """A class to raise when is not properly configured."""


class ImplementationError(PackageBaseException):

    """A class to raise when is not properly implemented."""


class CantBeRunError(PackageBaseException):

    """A class to raise when a application just cannot be run."""


class MissingDataError(PackageBaseException):

    """A class to raise when data is missing."""


class AutomationError(PackageBaseException):

    """A class to raise when automations fail."""
