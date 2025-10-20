import pytest
from decimal import Decimal
from datetime import datetime
from app.calculation import Calculation
from app.exceptions import OperationError
import logging

def test_addition():
    calc = Calculation(operation="add", operand1=Decimal("2"), operand2=Decimal("3"))
    assert calc.result == Decimal("5")

def test_subtraction():
    calc = Calculation(operation="subtract", operand1=Decimal("2"), operand2=Decimal("2"))
    assert calc.result == Decimal("0")

def test_multiplication():
    calc = Calculation(operation="multiply", operand1=Decimal("1"), operand2=Decimal("1"))
    assert calc.result == Decimal("1")

def test_division():
    calc = Calculation(operation="divide", operand1=Decimal("1"), operand2=Decimal("1"))
    assert calc.result == Decimal("1")

def test_division_by_zero():
    with pytest.raises(OperationError, match="Division by zero is not allowed"):
        Calculation(operation="divide", operand1=Decimal("1"), operand2=Decimal("0"))

def test_power():
    calc = Calculation(operation="Root", operand1=Decimal("16"), operand2=Decimal("2"))
    assert calc.result == Decimal("4")

def test_negative_power():
    with pytest.raises(OperationError, match="Negative exponents are not supported"):
        Calculation(operation="Power", operand1=Decimal("2"), operand2=Decimal("-3"))

def test_root():
    calc = Calculation(operation="Root", operand1=Decimal("16"), operand2=Decimal("2"))
    assert calc.result == Decimal("4")


def test_invalid_root():
    with pytest.raises(OperationError, match="Cannot calculate root of negative number"):
        Calculation(operation="Root", operand1=Decimal("-16"), operand2=Decimal("2"))


def test_unknown_operation():
    with pytest.raises(OperationError, match="Unknown operation"):
        Calculation(operation="Unknown", operand1=Decimal("5"), operand2=Decimal("3"))

def test_to_dict():
    calc = Calculation(operation="add", operand1=Decimal("2"), operand2=Decimal("3"))
    result_dict = calc.to_dict()
    assert result_dict == {
        "operation": "add",
        "operand1": "2",
        "operand2": "3",
        "result": "5",
        "timestamp": calc.timestamp.isoformat()
    }

def test_from_dict():
    data = {
        "operation": "add",
        "operand1": "2",
        "operand2": "3",
        "result": "5",
        "timestamp": datetime.now().isoformat()
    }
    calc = Calculation.from_dict(data)
    assert calc.operation == "add"
    assert calc.operand1 == Decimal("2")
    assert calc.operand2 == Decimal("3")
    assert calc.result == Decimal("5")


def test_invalid_from_dict():
    data = {
        "operation": "add",
        "operand1": "x",
        "operand2": "3",
        "result": "5",
        "timestamp": datetime.now().isoformat()
    }
    with pytest.raises(OperationError, match="Invalid calculation data"):
        Calculation.from_dict(data)

def test_format_result():
    calc = Calculation(operation="divide", operand1=Decimal("1"), operand2=Decimal("3"))
    assert calc.format_result(precision=2) == "0.33"
    assert calc.format_result(precision=9) == "0.333333333"


def test_equality():
    calc1 = Calculation(operation="add", operand1=Decimal("2"), operand2=Decimal("3"))
    calc2 = Calculation(operation="add", operand1=Decimal("2"), operand2=Decimal("3"))
    calc3 = Calculation(operation="subtract", operand1=Decimal("5"), operand2=Decimal("3"))
    assert calc1 == calc2
    assert calc1 != calc3

