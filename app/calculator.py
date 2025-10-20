from decimal import Decimal
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.input_validators import InputValidator

from app.operations import Operation
from app.exceptions import OperationError

class Calculator:
    def __init__(self, config: Optional[CalculatorConfig] = None):
        self.config = config or CalculatorConfig(base_dir=Path("."))
        self.history: List[Calculation] = []
        self.undo_stack: List[List[Calculation]] = []
        self.redo_stack: List[List[Calculation]] = []
        self.operation_strategy: Optional[Operation] = None

    def perform_operation(self, a: Decimal, b: Decimal) -> Decimal:
        if not self.operation_strategy:
            raise OperationError("No operation yet")
        
        a = InputValidator.validate_number(a, self.config)
        b = InputValidator.validate_number(b, self.config)

        result = self.operation_strategy.execute(a, b)
        
        calc = Calculation(
            operation=str(self.operation_strategy),
            operand1=a,
            operand2=b,
            result=result,
            timestamp=datetime.now()
        )
        self.history.append(calc)
        self.undo_stack.append(self.history.copy())
        self.redo_stack.clear()
        return result
    def set_operation(self, operation: Operation):
        self.operation_strategy = operation

    def undo(self) -> bool:
        if not self.undo_stack:
            return False
        self.redo_stack.append(self.history.copy())
        self.history = self.undo_stack.pop()
        return True
    
    def redo(self) -> bool:
        if not self.redo_stack:
            return False
        self.undo_stack.append(self.history.copy())
        self.history = self.redo_stack.pop()
        return True
    
    def show_history(self) -> List[str]:
        return [f"{c.operation}({c.operand1}, {c.operand2}) = {c.result}" for c in self.history]
    
    def clear_history(self):
        self.history.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()
