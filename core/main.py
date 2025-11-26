# core/main.py
from fastapi import FastAPI
from NiblitCore.core import core  # import your NiblitCore instance

app = FastAPI(title="Niblit AIOS")

@app.get("/")
def read_root():
    return {"message": "Niblit AIOS is online!"}

@app.get("/core/init")
def init_core():
    core.init()
    return {"status": "Core initialized"}

@app.get("/core/start")
def start_core():
    core.start()
    return {"status": "Core started"}

@app.get("/core/shutdown")
def shutdown_core():
    core.shutdown()
    return {"status": "Core shutdown"}

@app.post("/core/load_module/{module_name}")
def load_module(module_name: str, path: str):
    core.load_module(module_name, path)
    return {"status": f"Attempted to load module {module_name}"}
