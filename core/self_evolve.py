"""
Evolution engine: keeps simple scores and applies soft upgrades.
This is an extensible hook where more advanced model-training / code-gen can plug in.
"""
import logging, time, json, os
LOG = logging.getLogger("niblit.evolver")
BASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
STATE_FILE = os.path.join(BASE, "evolve_state.json")

class Evolver:
    def __init__(self, memory):
        self.memory = memory
        self.state = {"version": "0.1.0", "score": 0, "last_tick": 0}
        self._load()

    def _load(self):
        try:
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    self.state.update(json.load(f))
        except Exception as e:
            LOG.exception("Evolver load failed: %s", e)

    def _save(self):
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            LOG.exception("Evolver save failed: %s", e)

    def observe(self, event_type, details=None):
        # simple scoring heuristic
        if event_type == "user_feedback_positive":
            self.state["score"] += 5
        elif event_type == "user_feedback_negative":
            self.state["score"] -= 3
        elif event_type == "new_fact":
            self.state["score"] += 1
        self.state["last_tick"] = int(time.time())

    def decide_upgrade(self):
        # when score crosses threshold, propose a minor upgrade
        if self.state["score"] > 100:
            return {"action": "propose_codegen", "reason": "score_high"}
        if self.state["score"] < -50:
            return {"action": "run_heal", "reason": "low_score"}
        return None

    def apply_patch(self, patch_meta):
        # placeholder: record attempt
        LOG.info("Applying patch: %s", patch_meta)
        self.state["last_patch"] = {"meta": patch_meta, "ts": int(time.time())}
        self._save()

    def tick(self):
        # periodic tick; sample memory and build metrics
        nfacts = self.memory.count()
        self.state["score"] = max(-9999, min(9999, self.state.get("score",0) + nfacts//10))
        self.state["last_tick"] = int(time.time())
        self._save()

    def summary(self):
        return {"version": self.state.get("version"), "score": self.state.get("score")}
