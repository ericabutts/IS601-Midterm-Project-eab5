
#Exception hierarchy

class CalculatorError(Exception):
    """
    Base exception class for calculator errors
    """
    pass

class ValidationError(CalculatorError):
    """
    Raised when input validation fails
    """
    pass

class OperationError(CalculatorError):
    """
    Raised when a calculation operation fails
    """
    pass

class ConfigurationError(CalculatorError):
    """Raised when a calculation operation fails
    """
    pass