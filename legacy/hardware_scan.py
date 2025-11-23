"""
Scan for legacy devices (very simple).
"""
import os, logging, json
LOG = logging.getLogger("niblit.legacy.scan")

def scan_path(path="/sys"):
    findings = []
    try:
        for root, dirs, files in os.walk(path):
            for f in files:
                if "device" in f.lower() or "id" in f.lower():
                    findings.append(os.path.join(root, f))
            if len(findings) > 200:
                break
    except Exception as e:
        LOG.exception("Scan error: %s", e)
    return findings
