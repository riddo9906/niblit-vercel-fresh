# Niblit AIOS - lightweight dev README

This repository contains a modular Niblit prototype:
- `core/` : main runtime and evolution engine
- `engine/` : autonomy + reasoning layers
- `ui/` : minimal UI helpers (used by web frontend)
- `hardware/` : device & sensor adapters
- `integrations/` : legacy adapters & system bridges
- `storage/` : cache and tiny DB
- `data/` : external sources and realtime fetchers
- `legacy/` : legacy hardware migration blueprints

How to run (headless)

Integrate with FastAPI / web UI by calling `get_core()` and exposing `status()` + `/query` endpoints.
