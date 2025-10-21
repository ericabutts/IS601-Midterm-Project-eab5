import pytest
import logging
from app.history import LoggingObserver, AutoSaveObserver

class DummyCalc:
    def __init__(self, auto_save=True):
        class Config: pass
        self.config = Config()
        self.config.auto_save = auto_save
        self.save_history_called = False
    def save_history(self):
        self.save_history_called = True

def test_loggingobserver_raises_for_none():
    obs = LoggingObserver()
    with pytest.raises(AttributeError):
        obs.update(None)

def test_autosaveobserver_init_invalid_calculator():
    with pytest.raises(TypeError):
        AutoSaveObserver(object())  # Missing attributes

def test_autosaveobserver_updates_and_saves(monkeypatch):
    dummy = DummyCalc()
    obs = AutoSaveObserver(dummy)
    # Patch logging to prevent file writes
    monkeypatch.setattr(logging, "info", lambda msg: None)
    obs.update("not_none")
    assert dummy.save_history_called

def test_autosaveobserver_no_autosave(monkeypatch):
    dummy = DummyCalc(auto_save=False)
    obs = AutoSaveObserver(dummy)
    monkeypatch.setattr(logging, "info", lambda msg: None)
    obs.update("whatever")
    assert not dummy.save_history_called
