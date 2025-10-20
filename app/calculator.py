import pandas as pd
from decimal import Decimal
from pathlib import Path
from typing import List, Optional, Union
from datetime import datetime
import logging

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.input_validators import InputValidator
from app.operations import Operation
from app.exceptions import OperationError
from app.history import HistoryObserver
from app.calculator_memento import CalculatorMemento

Number = Union[int, float, Decimal]

class Calculator:
    def __init__(self, config: Optional[CalculatorConfig] = None):
        self.config = config or CalculatorConfig(base_dir=Path("."))
        self.history: List[Calculation] = []
        self.undo_stack: List[CalculatorMemento] = []
        self.redo_stack: List[CalculatorMemento] = []
        self.observers: List[HistoryObserver] = []
        self.operation_strategy: Optional[Operation] = None

        # Ensure history directory exists
        self.config.history_dir.mkdir(parents=True, exist_ok=True)
        
        logging.info("Calculator initialized with configuration")
        
        try:
            self.load_history()
        except Exception as e:
            logging.warning(f"Could not load existing history: {e}")

    def set_operation(self, operation: Operation):
        self.operation_strategy = operation
        logging.info(f"Operation set: {operation}")

    def add_observer(self, observer: HistoryObserver):
        self.observers.append(observer)

    def remove_observer(self, observer: HistoryObserver):
        self.observers.remove(observer)

    def notify_observers(self, calculation: Calculation):
        for obs in self.observers:
            obs.update(calculation)

    def perform_operation(self, a: Number, b: Number) -> Decimal:
        if not self.operation_strategy:
            raise OperationError("No operation set")

        validated_a = InputValidator.validate_number(a, self.config)
        validated_b = InputValidator.validate_number(b, self.config)

        result = self.operation_strategy.execute(validated_a, validated_b)

        calc = Calculation(
            operation=str(self.operation_strategy),
            operand1=validated_a,
            operand2=validated_b,
            result=result
        )



        # Save current state for undo/redo
        self.undo_stack.append(CalculatorMemento(self.history.copy()))
        self.redo_stack.clear()

        # Update history and notify observers
        self.history.append(calc)
        self.notify_observers(calc)

        return result

    def save_history(self) -> None:
        """Save history to CSV using pandas"""
        try:
            data = [{
                'operation': str(c.operation),
                'operand1': str(c.operand1),
                'operand2': str(c.operand2),
                'result': str(c.result),
                'timestamp': c.timestamp.isoformat()
            } for c in self.history]

            df = pd.DataFrame(data)
            df.to_csv(self.config.history_file, index=False)
            logging.info(f"History saved to {self.config.history_file}")
        except Exception as e:
            logging.error(f"Failed to save history: {e}")
            raise OperationError(f"Failed to save history: {e}")

    def load_history(self) -> None:
        """Load history from CSV using pandas"""
        try:
            if self.config.history_file.exists():
                df = pd.read_csv(self.config.history_file)
                self.history = [
                    Calculation.from_dict({
                        'operation': row['operation'],
                        'operand1': row['operand1'],
                        'operand2': row['operand2'],
                        'result': row['result'],
                        'timestamp': row['timestamp']
                    })
                    for _, row in df.iterrows()
                ]
                logging.info(f"Loaded {len(self.history)} calculations from history")
        except Exception as e:
            logging.error(f"Failed to load history: {e}")
            raise OperationError(f"Failed to load history: {e}")

    def undo(self) -> bool:
        if not self.undo_stack:
            return False
        memento = self.undo_stack.pop()
        self.redo_stack.append(CalculatorMemento(self.history.copy()))
        self.history = memento.history.copy()
        return True

    def redo(self) -> bool:
        if not self.redo_stack:
            return False
        memento = self.redo_stack.pop()
        self.undo_stack.append(CalculatorMemento(self.history.copy()))
        self.history = memento.history.copy()
        return True

    def show_history(self) -> List[str]:
        return [f"{c.operation}({c.operand1}, {c.operand2}) = {c.result}" for c in self.history]

    def clear_history(self):
        self.history.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()
        logging.info("History cleared")
