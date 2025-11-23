"""
Voice helper wrapper. At runtime it tries to use local TTS,
but it's safe if not available.
"""
import logging, subprocess, shlex

LOG = logging.getLogger("niblit.voice")

def tts(text):
    # try common linux tts commands
    for cmd in ("espeak", "say", "termux-tts-speak"):
        try:
            p = shlex.split(f"{cmd} \"{text}\"")
            subprocess.run(p, timeout=8)
            return True
        except Exception:
            continue
    LOG.debug("No TTS available for: %s", text)
    return False
