"""
Lightweight terminal + web UI helpers.
Terminal renderer falls back to text; web UI reads the same status files.
"""
import logging, json, os
LOG = logging.getLogger("niblit.ui.display")
BASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
STATUS_FILE = os.path.join(BASE, "status.json")

def write_status(obj):
    try:
        with open(STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2)
    except Exception as e:
        LOG.exception("Write status failed: %s", e)

def read_status():
    try:
        if os.path.exists(STATUS_FILE):
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        LOG.exception("Read status failed: %s", e)
    return {}
