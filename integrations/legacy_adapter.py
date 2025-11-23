"""
Adapter to connect legacy hardware/software interfaces.
Lightweight: translates old configs to new structure.
"""
import logging, json, os

LOG = logging.getLogger("niblit.legacy")

def adapt_config(legacy_cfg_path):
    try:
        with open(legacy_cfg_path, "r", encoding="utf-8") as f:
            raw = f.read()
        # Very naive: look for KEY=VALUE lines
        out = {}
        for line in raw.splitlines():
            if "=" in line:
                k,v = line.split("=",1)
                out[k.strip()] = v.strip()
        LOG.info("Adapted legacy config with %d keys", len(out))
        return out
    except Exception as e:
        LOG.exception("Legacy adapt failed: %s", e)
        return {}
