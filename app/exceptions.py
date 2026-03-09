"""Custom exception hierarchy for the calculator application."""

class CalculatorError(Exception):
    """Base exception for all calculator errors."""
    pass

class ValidationError(CalculatorError):
    """Raised when input validation fails."""
    pass

class OperationError(CalculatorError):
    """Raised when an arithmetic operation fails."""
    pass

class ConfigurationError(CalculatorError):
    """Raised when configuration is invalid."""
    pass