"""
Minimal unit smoke tests (run locally with pytest if you like).
"""
from core.main import get_core

def test_core_start_stop():
    c = get_core()
    c.start()
    assert c.running
    c.stop()
    assert not c.running
