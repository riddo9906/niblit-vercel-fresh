"""
Niblit Core entrypoint (headless).
Starts core systems and exposes a lightweight API object.
"""
import logging, threading, time, os
from datetime import datetime
from .memory import MemoryManager
from .self_evolve import Evolver
from engine.autonomy import AutonomyEngine
from engine.logic import LogicEngine

LOG = logging.getLogger("niblit.core")
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

STATE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "state.json")

class NiblitCore:
    def __init__(self):
        LOG.info("Starting NiblitCore...")
        self.start_time = datetime.utcnow()
        self.memory = MemoryManager()
        self.evolver = Evolver(self.memory)
        self.logic = LogicEngine(self.memory)
        self.autonomy = AutonomyEngine(self.logic, self.evolver, self.memory)
        self.running = False
        self._bg = None

    def start(self):
        if self.running:
            return
        self.running = True
        LOG.info("NiblitCore: starting background loop")
        self._bg = threading.Thread(target=self._loop, daemon=True, name="niblit-core-loop")
        self._bg.start()

    def _loop(self):
        while self.running:
            try:
                # periodic tick: sense -> think -> act -> persist
                self.autonomy.tick()
                self.evolver.tick()
                self.memory.autosave()
            except Exception as e:
                LOG.exception("Core loop error: %s", e)
            time.sleep(2)

    def stop(self):
        LOG.info("Stopping NiblitCore...")
        self.running = False
        if self._bg:
            self._bg.join(timeout=2)
        self.memory.autosave()
        LOG.info("NiblitCore stopped.")

    def status(self):
        uptime = (datetime.utcnow() - self.start_time).total_seconds()
        return {
            "uptime_s": int(uptime),
            "memory_entries": self.memory.count(),
            "evolve_state": self.evolver.summary(),
        }

# convenience factory
_core = None
def get_core():
    global _core
    if _core is None:
        _core = NiblitCore()
    return _core

if __name__ == "__main__":
    core = get_core()
    core.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        core.stop()
