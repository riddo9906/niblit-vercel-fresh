# Vercel serverless entry point for /api/commands
# Imports the Flask WSGI app from app.py so Vercel can serve this route
# as an independent serverless function.
from app import app
