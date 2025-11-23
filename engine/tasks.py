"""
Task subsystem: queue + simple scheduler for longer tasks.
"""
import time, threading, logging, queue

LOG = logging.getLogger("niblit.tasks")

class TaskScheduler:
    def __init__(self):
        self.q = queue.Queue()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def add(self, fn, *args, **kwargs):
        self.q.put((fn, args, kwargs))

    def _loop(self):
        while True:
            try:
                fn, args, kwargs = self.q.get()
                try:
                    fn(*args, **kwargs)
                except Exception as e:
                    LOG.exception("Task failed: %s", e)
            except Exception as e:
                LOG.exception("Scheduler loop error: %s", e)
            time.sleep(0.1)
