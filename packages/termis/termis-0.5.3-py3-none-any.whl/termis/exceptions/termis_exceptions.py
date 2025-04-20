"""Custom exceptions for the Termis application."""

class TermisException(Exception):
    """Base exception for termis-specific errors."""
    pass

class DryRunException(TermisException):
    """Raised when in dry-run mode to prevent actual execution."""
    pass

class ConfigurationError(TermisException):
    """Raised when there are configuration-related errors."""
    pass

class ToolIntegrationError(TermisException):
    """Raised when there are errors with external tool integrations."""
    pass