"""
Device detection & simple sensor emulation.
Exposes a Sensors object with refresh() and read() so it can be used by older code.
"""
import logging, random, time
LOG = logging.getLogger("niblit.device")

class Sensors:
    def __init__(self):
        LOG.info("Sensors: initializing")
        self.status = {"gps": None, "camera": False, "mic": False, "last_update": None}
        self._running = False

    def refresh(self):
        # safe to call repeatedly
        try:
            self.status["gps"] = {"lat": round(-33.93 + random.uniform(-0.02,0.02),4),
                                  "lon": round(18.42 + random.uniform(-0.02,0.02),4)}
            self.status["camera"] = False
            self.status["mic"] = False
            self.status["last_update"] = time.strftime("%Y-%m-%d %H:%M:%S")
            LOG.debug("Sensors refreshed: %s", self.status)
        except Exception as e:
            LOG.exception("Sensor refresh failed: %s", e)

    def read(self):
        # return snapshot
        return dict(self.status)
