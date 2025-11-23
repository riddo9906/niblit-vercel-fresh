"""
Logic engine: lightweight reasoning rules + pattern detection.
This is a place to add advanced reasoning, knowledge graphs, or LLM adapters.
"""
import logging, random

LOG = logging.getLogger("niblit.logic")

class LogicEngine:
    def __init__(self, memory):
        self.memory = memory

    def decide(self, recent_history):
        # Very small example heuristics:
        # - If user asked a question (role == user and contains '?') -> reply log
        # - If many repeated facts -> summarize
        for msg in recent_history:
            txt = msg.get("text","").lower()
            if msg.get("role") == "user":
                if "remember" in txt:
                    # try to parse "remember key: value"
                    try:
                        _, rest = txt.split(" ",1)
                        k,v = rest.split(":",1)
                        return {"type":"remember", "key":k.strip(), "value":v.strip()}
                    except Exception:
                        pass
                if txt.endswith("?"):
                    return {"type":"log", "message":"User asked a question: "+txt}
        # default small chance to noop or log
        if random.random() < 0.05:
            return {"type":"log", "message":"Autonomy heartbeat"}
        return {"type":"noop"}
