"""
Minimal web-friendly JSON UI layer (used by simple frontend).
"""
from core.main import get_core

def status_payload():
    core = get_core()
    return core.status()
