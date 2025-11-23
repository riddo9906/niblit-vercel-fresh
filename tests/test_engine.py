from engine.logic import LogicEngine
from core.memory import MemoryManager

def test_logic_remember():
    mem = MemoryManager(path="data/test_memory.json")
    logic = LogicEngine(mem)
    # a user remember command should produce a remember action
    action = logic.decide([{"role":"user","text":"remember fav: pizza"}])
    assert action["type"] == "remember"
