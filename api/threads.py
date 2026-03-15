# Vercel serverless entry point for /api/threads
# The Flask WSGI app is loaded via a factory function so that Vercel's
# static analysis (isPythonEntrypoint / containsAppOrHandler) detects
# the top-level `app = <call>` pattern and registers this file as a
# valid Serverless Function entry point.
from app import app as _wsgi_app


def _get_app():
    return _wsgi_app


app = _get_app()
