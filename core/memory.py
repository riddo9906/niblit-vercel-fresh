"""
Simple persistent memory manager using JSON file.
Supports set/get/list for small facts and chat history.
"""
import json, os, threading, time, logging

LOG = logging.getLogger("niblit.memory")
BASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(BASE, exist_ok=True)
MEM_FILE = os.path.join(BASE, "memory.json")

class MemoryManager:
    def __init__(self, path=MEM_FILE):
        self.path = path
        self.lock = threading.RLock()
        self._data = {"facts": [], "history": []}
        self._load()

    def _load(self):
        try:
            if os.path.exists(self.path):
                with open(self.path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
                    LOG.info("Memory loaded: %d facts", len(self._data.get("facts",[])))
        except Exception as e:
            LOG.exception("Memory load failed: %s", e)
            self._data = {"facts": [], "history": []}

    def autosave(self):
        try:
            with self.lock:
                with open(self.path, "w", encoding="utf-8") as f:
                    json.dump(self._data, f, indent=2)
        except Exception as e:
            LOG.exception("Memory autosave failed: %s", e)

    def set(self, key, value):
        with self.lock:
            self._data.setdefault("facts", []).append({"key": key, "value": value, "ts": int(time.time())})

    def list_facts(self, limit=20):
        with self.lock:
            return list(reversed(self._data.get("facts", [])))[:limit]

    def add_history(self, role, text):
        with self.lock:
            self._data.setdefault("history", []).append({"role": role, "text": text, "ts": int(time.time())})
            # trim to last 200
            self._data["history"] = self._data["history"][-200:]

    def history(self, limit=50):
        with self.lock:
            return list(reversed(self._data.get("history", [])))[:limit]

    def count(self):
        with self.lock:
            return len(self._data.get("facts", []))
