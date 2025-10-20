# CALCULATION 

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal, InvalidOperation
import logging
from typing import Any, Dict

from app.exceptions import OperationError


@dataclass
class Calculation:
    """
    Value Object representing a single calculation.
    """

    operation: str   
    operand1: Decimal
    operand2: Decimal
    result: Decimal = None
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """
        Calculate the result after initialization if not provided.
        """
        if self.result is None:
            self.result = self._compute_result()

    def _compute_result(self) -> Decimal:
        """
        Compute the result based on the operation and operands.
        """
        operation_map = {
            'add': lambda a, b: a + b,
            'subtract': lambda a, b: a - b,
            'multiply': lambda a, b: a * b,
            'divide': self._divide,
            'power': self._power,
            'root': self._root
        }
        
        operation_func = operation_map.get(self.operation.lower())
        if not operation_func:
            raise OperationError(f"Unknown operation: {self.operation}")
        
        return operation_func(self.operand1, self.operand2)

    def _divide(self, a: Decimal, b: Decimal) -> Decimal:
        """Handle division with zero check"""
        if b == 0:
            self._raise_div_zero()
        return a / b

    def _power(self, a: Decimal, b: Decimal) -> Decimal:
        """Handle power operation with negative exponent check."""
        if b < 0:
            self._raise_neg_power()
        return Decimal(pow(float(a), float(b)))

    def _root(self, a: Decimal, b: Decimal) -> Decimal:
        """Handle root operation with validation."""
        if b == 0:
            self._raise_invalid_root(a, b)
        if a < 0:
            self._raise_invalid_root(a, b)
        return Decimal(pow(float(a), 1 / float(b)))

    @staticmethod
    def _raise_div_zero():  # pragma: no cover
        """
        Helper method to raise division by zero error.
        """
        raise OperationError("Division by zero is not allowed")

    @staticmethod
    def _raise_neg_power():  # pragma: no cover
        """
        Helper method to raise negative power error.
        """
        raise OperationError("Negative exponents are not supported")

    @staticmethod
    def _raise_invalid_root(x: Decimal, y: Decimal):  # pragma: no cover
        """
        Helper method to raise invalid root error.
        """
        if y == 0:
            raise OperationError("Zero root is undefined")
        if x < 0:
            raise OperationError("Cannot calculate root of negative number")
        raise OperationError("Invalid root operation")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert calculation to dictionary for serialization.
        """
        return {
            'operation': self.operation,
            'operand1': str(self.operand1),
            'operand2': str(self.operand2),
            'result': str(self.result),
            'timestamp': self.timestamp.isoformat()
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Calculation':
        """
        Create calculation from dictionary.
        """
        try:
            # Create the calculation object with the original operands
            calc = Calculation(
                operation=data['operation'],
                operand1=Decimal(data['operand1']),
                operand2=Decimal(data['operand2']),
                result=Decimal(data['result']),
                timestamp=datetime.fromisoformat(data['timestamp'])
            )

            # Verify the result matches (helps catch data corruption)
            saved_result = Decimal(data['result'])
            if calc.result != saved_result:
                logging.warning(
                    f"Loaded calculation result {saved_result} "
                    f"differs from computed result {calc.result}"
                )  # pragma: no cover

            return calc

        except (KeyError, InvalidOperation, ValueError) as e:
            raise OperationError(f"Invalid calculation data: {str(e)}")

    def __str__(self) -> str:
        """
        Return string representation of calculation.
        """
        return f"{self.operation}({self.operand1}, {self.operand2}) = {self.result}"

    def __repr__(self) -> str:
        """
        Return detailed string representation of calculation.
        """
        return (
            f"Calculation(operation='{self.operation}', "
            f"operand1={self.operand1}, "
            f"operand2={self.operand2}, "
            f"result={self.result}, "
            f"timestamp='{self.timestamp.isoformat()}')"
        )

    def __eq__(self, other: object) -> bool:
        """
        Check if two calculations are equal.
        """
        if not isinstance(other, Calculation):
            return NotImplemented
        return (
            self.operation == other.operation and
            self.operand1 == other.operand1 and
            self.operand2 == other.operand2 and
            self.result == other.result
        )

    def format_result(self, precision: int = 10) -> str:
        """
        Format the calculation result with specified precision.
        """
        try:
            # Remove trailing zeros and format to specified precision
            return str(self.result.normalize().quantize(
                Decimal('0.' + '0' * precision)
            ).normalize())
        except InvalidOperation:  # pragma: no cover
            return str(self.result)