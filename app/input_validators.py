from decimal import Decimal
from app.exceptions import ValidationError

class InputValidator:
    @staticmethod
    def validate_number(value, config):
        """Convert input to Decimal and enforce limits."""
        try:
            num = Decimal(str(value))
        except Exception:
            raise ValidationError(f"Invalid number: {value}")

        if abs(num) > config.max_input_value:
            raise ValidationError(f"Value {num} exceeds maximum {config.max_input_value}")
        return num
