import pytest
from app.operations import OperationFactory

def test_unknown_operation():
    with pytest.raises(ValueError):
        OperationFactory.create_operation("unknown_op")
