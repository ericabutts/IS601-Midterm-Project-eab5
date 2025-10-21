import pytest
from io import StringIO
from app.calculator_repl import calculator_repl  


def run_repl_with_inputs(monkeypatch, inputs):
    """
    To simulate REPL input sequence.
    'inputs' should be a list of strings (each simulates an Enter key press).
    """
    # Convert list of inputs into an iterator for monkeypatch
    input_iter = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_iter))
    # Capture printed output
    with pytest.raises(SystemExit):
        calculator_repl()


def test_help_command(monkeypatch, capsys):
    """Test that the 'help' command prints the help text and continues."""
    inputs = ["help", "exit"]
    input_iter = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_iter))

    # Run REPL once
    calculator_repl()

    captured = capsys.readouterr()
    assert "Available commands" in captured.out
    assert "Goodbye" in captured.out


def test_unknown_command(monkeypatch, capsys):
    """Test how REPL handles unknown commands."""
    inputs = ["x", "exit"]
    input_iter = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_iter))

    calculator_repl()

    captured = capsys.readouterr()
    assert "Unknown command" in captured.out
    assert "Goodbye" in captured.out


def test_add_operation(monkeypatch, capsys):
    """Simulate a valid add operation."""
    inputs = [
        "add",
        "2",       # First number
        "3",       # Second number
        "exit"
    ]
    input_iter = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_iter))

    calculator_repl()
    captured = capsys.readouterr()

    assert "Result" in captured.out
    assert "5" in captured.out


def test_cancel_operation(monkeypatch, capsys):
    """Simulate cancelling an operation."""
    inputs = [
        "add",
        "cancel",  # Cancels before entering first number
        "exit"
    ]
    input_iter = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_iter))

    calculator_repl()
    captured = capsys.readouterr()

    assert "Operation cancelled" in captured.out
    assert "Goodbye" in captured.out


@pytest.fixture
def fake_calc_ex(monkeypatch):
    """Fake calculator that can raise errors for coverage."""
    class FakeCalc:
        def __init__(self):
            class Cfg: auto_save = True
            self.config = Cfg()
        def add_observer(self, o): pass
        def show_history(self): return []
        def clear_history(self): pass
        def undo(self): return False
        def redo(self): return False
        def save_history(self): raise Exception("save failed")
        def load_history(self): raise Exception("load failed")
        def set_operation(self, op): pass
        def perform_operation(self, a, b): raise ValueError("bad op")
    monkeypatch.setattr("app.calculator_repl.Calculator", lambda: FakeCalc())
    monkeypatch.setattr("app.calculator_repl.OperationFactory",
                        type("F", (), {"create_operation": staticmethod(lambda x: x)}))
    monkeypatch.setattr("app.calculator_repl.LoggingObserver", lambda *a, **k: None)
    monkeypatch.setattr("app.calculator_repl.AutoSaveObserver", lambda *a, **k: None)
    return FakeCalc()

@pytest.fixture
def fake_calc(monkeypatch):
    """Basic fake calculator for normal REPL tests."""
    class FakeCalc:
        def __init__(self):
            class Config:
                auto_save = True
            self.config = Config()
            self.history = []
            self.undo_called = False
            self.redo_called = False

        def add_observer(self, o): pass
        def show_history(self): return self.history
        def clear_history(self): self.history.clear()
        def undo(self):
            self.undo_called = True
            return True
        def redo(self):
            self.redo_called = True
            return True
        def save_history(self): print("History saved successfully")
        def load_history(self): print("History loaded successfully")
        def set_operation(self, op): pass
        def perform_operation(self, a, b): return 42  # mock result

    monkeypatch.setattr("app.calculator_repl.Calculator", lambda: FakeCalc())
    monkeypatch.setattr("app.calculator_repl.OperationFactory",
                        type("FakeFactory", (), {"create_operation": staticmethod(lambda x: x)}))
    monkeypatch.setattr("app.calculator_repl.LoggingObserver", lambda *a, **k: None)
    monkeypatch.setattr("app.calculator_repl.AutoSaveObserver", lambda *a, **k: None)
    return FakeCalc()


def run_inputs(monkeypatch, seq):
    it = iter(seq)
    monkeypatch.setattr("builtins.input", lambda _: next(it))
    calculator_repl()

def test_save_load_exceptions(monkeypatch, capsys, fake_calc_ex):
    run_inputs(monkeypatch, ["save", "load", "exit"])
    out = capsys.readouterr().out
    assert "Error saving" in out or "Error loading" in out

def test_undo_redo_nothing(monkeypatch, capsys, fake_calc_ex):
    run_inputs(monkeypatch, ["undo", "redo", "exit"])
    out = capsys.readouterr().out
    assert "Nothing to undo" in out or "Nothing to redo" in out

def test_operation_error(monkeypatch, capsys, fake_calc_ex):
    run_inputs(monkeypatch, ["add", "2", "3", "exit"])
    out = capsys.readouterr().out
    assert "Unexpected error" in out or "Error" in out


def run_inputs(monkeypatch, inputs):
    it = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(it))
    calculator_repl()


def test_history_command(monkeypatch, capsys, fake_calc):
    run_inputs(monkeypatch, ["history", "exit"])
    out = capsys.readouterr().out
    assert "No calculations" in out or "Calculation History" in out


def test_clear_command(monkeypatch, capsys, fake_calc):
    run_inputs(monkeypatch, ["clear", "exit"])
    out = capsys.readouterr().out
    assert "History cleared" in out


def test_undo_and_redo(monkeypatch, capsys, fake_calc):
    run_inputs(monkeypatch, ["undo", "redo", "exit"])
    out = capsys.readouterr().out
    assert "undone" in out
    assert "redone" in out


def test_save_and_load(monkeypatch, capsys, fake_calc):
    run_inputs(monkeypatch, ["save", "load", "exit"])
    out = capsys.readouterr().out
    assert "saved" in out
    assert "loaded" in out


def test_exit_saves_history(monkeypatch, capsys, fake_calc):
    run_inputs(monkeypatch, ["exit"])
    out = capsys.readouterr().out
    assert "History saved" in out or "Goodbye" in out


def test_add_operation_success(monkeypatch, capsys, fake_calc):
    run_inputs(monkeypatch, ["add", "2", "3", "exit"])
    out = capsys.readouterr().out
    assert "Result" in out
    assert "42" in out  # Mocked perform_operation


def test_add_operation_cancel(monkeypatch, capsys, fake_calc):
    run_inputs(monkeypatch, ["add", "cancel", "exit"])
    out = capsys.readouterr().out
    assert "Operation cancelled" in out
