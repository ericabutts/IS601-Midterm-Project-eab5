
class HistoryObserver:
    def update(self, calculation):
        print(f"Observer notified {calculation.operation} -> {calculation.result}")