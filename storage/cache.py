"""
Simple in-memory + disk-backed cache for transient items.
"""
import time, json, os, threading, logging
LOG = logging.getLogger("niblit.cache")
BASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(BASE, exist_ok=True)
CACHE_FILE = os.path.join(BASE, "cache.json")

class Cache:
    def __init__(self):
        self.lock = threading.RLock()
        self._map = {}
        self._load()

    def _load(self):
        try:
            if os.path.exists(CACHE_FILE):
                with open(CACHE_FILE,"r",encoding="utf-8") as f:
                    self._map = json.load(f)
        except Exception as e:
            LOG.debug("Cache load failed: %s", e)

    def set(self, k, v, ttl=None):
        with self.lock:
            self._map[k] = {"value": v, "ts": int(time.time()), "ttl": ttl}
            self._save()

    def get(self, k, default=None):
        with self.lock:
            rec = self._map.get(k)
            if not rec:
                return default
            if rec.get("ttl") and int(time.time()) - rec.get("ts",0) > rec["ttl"]:
                del self._map[k]
                self._save()
                return default
            return rec["value"]

    def _save(self):
        try:
            with open(CACHE_FILE,"w",encoding="utf-8") as f:
                json.dump(self._map,f,indent=2)
        except Exception as e:
            LOG.debug("Cache save failed: %s", e)
