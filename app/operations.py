from decimal import Decimal
from app.exceptions import OperationError

class Operation:
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        raise NotImplementedError
    
class AddOperation(Operation):
    def __str__(self):
        return "add"
    def execute(self, a, b):
        return a + b
    
class SubtractOperation(Operation):
    def __str__(self):
        return "subtract"
    def execute(self, a, b):
        return a - b
    
class MultiplyOperation(Operation):
    def __str__(self):
        return "multiply"
    def execute(self, a, b):
        return a * b
    
class DivideOperation(Operation):
    def __str__(self):
        return "divide"
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Division by zero")
        return a / b