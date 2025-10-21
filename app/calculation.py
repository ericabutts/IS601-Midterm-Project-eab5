# CALCULATION 

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal, InvalidOperation
import logging
from typing import Any, Dict

from app.exceptions import OperationError
from app.operations import OperationFactory


@dataclass
class Calculation:
    """
    Object representing a single calculation.
    """

    operation: str   
    operand1: Decimal
    operand2: Decimal
    result: Decimal = None
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """
        Calculate result after initialization if not provided.
        """
        if self.result is None:
            self.result = self._compute_result()

    def _compute_result(self) -> Decimal:
        """
        Compute the result using the Operation classes.
        This delegates to the Operation strategy pattern instead of duplicating logic.
        """
        try:
            # Use the OperationFactory to get the appropriate operation
            operation_instance = OperationFactory.create_operation(self.operation)
            return operation_instance.execute(self.operand1, self.operand2)
        except ValueError as e:
            # OperationFactory raises ValueError for unknown operations
            raise OperationError(str(e))

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
            # Store the saved result for comparison
            saved_result = Decimal(data['result'])
            
            # Create the calculation object with the saved result
            calc = Calculation(
                operation=data['operation'],
                operand1=Decimal(data['operand1']),
                operand2=Decimal(data['operand2']),
                result=saved_result,
                timestamp=datetime.fromisoformat(data['timestamp'])
            )

            # Compute what the result should be
            computed_result = calc._compute_result()
            
            # Verify the saved result matches the computed result
            if saved_result != computed_result:
                logging.warning(
                    f"Loaded calculation result {saved_result} "
                    f"differs from computed result {computed_result}"
                )

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