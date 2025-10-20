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