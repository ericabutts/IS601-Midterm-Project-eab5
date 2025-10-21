import pytest
from app.exceptions import CalculatorError, ValidationError, OperationError, ConfigurationError

def test_calculator_error_is_base_exception():
    with pytest.raises(CalculatorError) as exc_info:
        raise CalculatorError("Base calculator error occurred")
    assert str(exc_info.value) == "Base calculator error occurred"