"""
Autonomy engine: orchestrates a simple sense->plan->act pipeline.
"""
import logging, time
LOG = logging.getLogger("niblit.autonomy")

class AutonomyEngine:
    def __init__(self, logic_engine, evolver, memory_manager):
        self.logic = logic_engine
        self.evolver = evolver
        self.memory = memory_manager
        self._last_tick = 0

    def tick(self):
        # sense: read short history
        hist = self.memory.history(10)
        # plan: ask logic engine for an action
        action = self.logic.decide(hist)
        # act: carry out action
        if action:
            self._perform(action)
        self._last_tick = time.time()

    def _perform(self, action):
        try:
            typ = action.get("type")
            if typ == "remember":
                self.memory.set(action.get("key","auto"), action.get("value",""))
                self.evolver.observe("new_fact")
                LOG.info("Autonomy: remembered %s", action.get("key"))
            elif typ == "log":
                LOG.info("Autonomy log: %s", action.get("message"))
            elif typ == "noop":
                pass
            else:
                LOG.info("Autonomy received unknown action: %s", action)
        except Exception as e:
            LOG.exception("Autonomy perform error: %s", e)
