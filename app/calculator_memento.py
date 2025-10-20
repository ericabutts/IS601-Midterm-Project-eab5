from dataclasses import dataclass, field
import datetime
from typing import Any, Dict, List

from app.calculation import Calculation


@dataclass
class CalculatorMemento:
    """
    MEMENTO pattern allows for undo/redo functions
    """

    history: List[Calculation]  # List of Calculation instances representing the calculator's history
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)  # Time when the memento was created

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes memento into dictionary. Returns a dictionary containing the serialized state of the memento.
        """
        return {
            'history': [calc.to_dict() for calc in self.history],
            'timestamp': self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CalculatorMemento':
        """
        Creates new memento from dictionary
        """
        return cls(
            history=[Calculation.from_dict(calc) for calc in data['history']],
            timestamp=datetime.datetime.fromisoformat(data['timestamp'])
        )
