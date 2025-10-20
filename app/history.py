from abc import ABC, abstractmethod
import logging
from typing import Any
from app.calculation import Calculation


class HistoryObserver(ABC):
    @abstractmethod
    def update(self, calculation: Calculation):
        """Handle new calculation"""
        pass # pragma: no cover

class LoggingObserver(HistoryObserver):
    """Observer that logs calculations to file"""
    def update(self, calculation: Calculation) -> None:
        if calculation is None:
            raise AttributeError("Calculation cannont be none")
        logging.info(
            f"Calculation performed: {calculation.operation} "
            f"({calculation.operand1}, {calculation.operand2}) = "
            f"{calculation.result}"
        )

class AutoSaveObserver(HistoryObserver):
    """Observer that automatically saves calculations"""
    def __init__(self, calculator: Any):
        if not hasattr(calculator, 'config') or not hasattr(calculator, 'save_history'):
            raise TypeError("Calculator must have config and save history attributes")
        self.calculator = calculator

    def update(self, calculation: Calculation) -> None:
        """ Observer to trigger autosave"""
        if calculation is None:
            raise AttributeError("Calculation cannot be None")
        if self.calculator.config.auto_save:
            self.calculator.save_history()
            logging.info("History auto-saved")