"""
Realtime data ingestion helpers.
These functions provide adapters to collect polling data from web endpoints.
"""
import requests, logging, time
LOG = logging.getLogger("niblit.realtime")

def fetch_json(url, timeout=6):
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        LOG.debug("fetch_json fail %s: %s", url, e)
        return None
