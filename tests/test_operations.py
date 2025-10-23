import pytest
from decimal import Decimal
from app.operations import OperationFactory
from app.exceptions import OperationError
from app.operations import (
    RootOperation,
    ModulusOperation,
    IntegerDivisionOperation,
    PercentageOperation,
    AbsoluteDifferenceOperation,
)

def test_unknown_operation():
    with pytest.raises(ValueError):
        OperationFactory.create_operation("unknown_op")

def test_root_operation_valid():
    op = RootOperation()
    result = op.execute(Decimal('9'), Decimal('2'))  # sqrt(9)
    assert round(result, 5) == Decimal('3.0')

def test_root_operation_zero_root():
    op = RootOperation()
    with pytest.raises(OperationError, match="Zero root is undefined"):
        op.execute(Decimal('9'), Decimal('0'))

def test_root_operation_negative_number():
    op = RootOperation()
    with pytest.raises(OperationError, match="Cannot calculate root of negative number"):
        op.execute(Decimal('-9'), Decimal('2'))


def test_modulus_operation_valid():
    op = ModulusOperation()
    result = op.execute(Decimal('10'), Decimal('3'))
    assert result == Decimal('1')

def test_modulus_operation_division_by_zero():
    op = ModulusOperation()
    with pytest.raises(OperationError, match="Division by zero"):
        op.execute(Decimal('10'), Decimal('0'))


def test_integer_division_valid():
    op = IntegerDivisionOperation()
    result = op.execute(Decimal('10'), Decimal('2'))
    assert result == Decimal('5')

def test_integer_division_divide_by_zero():
    op = IntegerDivisionOperation()
    with pytest.raises(OperationError, match="Division by zero"):
        op.execute(Decimal('10'), Decimal('0'))


def test_percentage_operation_valid():
    op = PercentageOperation()
    result = op.execute(Decimal('1'), Decimal('4'))
    assert result == Decimal('25')  

def test_percentage_operation_divide_by_zero():
    op = PercentageOperation()
    with pytest.raises(OperationError, match="Division by zero"):
        op.execute(Decimal('5'), Decimal('0'))


def test_absolute_difference_positive_result():
    op = AbsoluteDifferenceOperation()
    result = op.execute(Decimal('10'), Decimal('6'))
    assert result == Decimal('4')

def test_absolute_difference_negative_result():
    op = AbsoluteDifferenceOperation()
    result = op.execute(Decimal('3'), Decimal('7'))
    assert result == Decimal('4')