"""
Tiny JSON DB for structured records.
"""
import json, os, threading, logging
LOG = logging.getLogger("niblit.db")
BASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DB_FILE = os.path.join(BASE, "db.json")
os.makedirs(BASE, exist_ok=True)

class TinyDB:
    def __init__(self, path=DB_FILE):
        self.path = path
        self.lock = threading.RLock()
        self._data = {"records": []}
        self._load()

    def _load(self):
        try:
            if os.path.exists(self.path):
                with open(self.path,"r",encoding="utf-8") as f:
                    self._data = json.load(f)
        except Exception as e:
            LOG.debug("DB load failed: %s", e)

    def insert(self, obj):
        with self.lock:
            self._data.setdefault("records",[]).append(obj)
            self._save()

    def find(self, predicate):
        with self.lock:
            return [r for r in self._data.get("records",[]) if predicate(r)]

    def _save(self):
        try:
            with open(self.path,"w",encoding="utf-8") as f:
                json.dump(self._data,f,indent=2)
        except Exception as e:
            LOG.debug("DB save failed: %s", e)
