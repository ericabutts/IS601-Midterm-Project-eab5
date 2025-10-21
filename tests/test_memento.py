from app.calculator_memento import CalculatorMemento
from app.calculation import Calculation
import datetime

def test_memento_to_dict_and_from_dict():
    # Create a fake Calculation (minimal structure)
    calc = Calculation(operation="add", operand1=1, operand2=2, result=3)
    memento = CalculatorMemento(history=[calc])
    data = memento.to_dict()

    # Verify serialization keys
    assert "history" in data
    assert "timestamp" in data
    assert isinstance(data["history"], list)

    # Deserialize back to a new memento
    restored = CalculatorMemento.from_dict(data)
    assert isinstance(restored, CalculatorMemento)
    assert len(restored.history) == 1
    assert restored.history[0].operation == "add"
    assert isinstance(restored.timestamp, datetime.datetime)


def test_memento_empty_history_to_dict():
    memento = CalculatorMemento(history=[])
    data = memento.to_dict()
    assert data["history"] == []
    assert "timestamp" in data
