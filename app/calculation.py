from decimal import Decimal
from datetime import datetime

class Calculation:
    def __init__(self, operation: str, operand1: Decimal, operand2: Decimal, result: Decimal = None, timestamp=None):
        self.operation = operation
        self.operand1 = operand1
        self.operand2 = operand2
        self.result = result or Decimal("0")
        self.timestamp = timestamp or datetime or datetime.now()
        
    @classmethod
    def from_dict(cls, data: dict):
        """
        Recreate calculation from dictionary
        """
        from decimal import Decimal
        from datetime import datetime
        return cls(
            operation=data.get("operation"),
            operand1=Decimal(data.get("operand1")),
            operand2=Decimal(data.get("operand2")),
            result=Decimal(data.get("result")),
            timestamp=datetime.fromisoformat(data.get("timestamp")),
        )
    
    