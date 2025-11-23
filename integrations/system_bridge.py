"""
System bridge: run safe system commands and gather info.
Used selectively; environment-safe.
"""
import logging, subprocess, shlex

LOG = logging.getLogger("niblit.bridge")

def run(cmd, timeout=8):
    try:
        parts = shlex.split(cmd)
        r = subprocess.run(parts, capture_output=True, text=True, timeout=timeout)
        return {"code": r.returncode, "stdout": r.stdout.strip(), "stderr": r.stderr.strip()}
    except Exception as e:
        LOG.exception("Bridge run failed: %s", e)
        return {"code": -1, "stdout": "", "stderr": str(e)}
