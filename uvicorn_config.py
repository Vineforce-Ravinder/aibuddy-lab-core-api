"""Uvicorn configuration file for development.

Usage:
    uvicorn app.main:app --config-path uvicorn_config.py
    or
    python -c "import uvicorn; uvicorn.run(config=uvicorn.Config('app.main:app', **config))"
"""

host = "127.0.0.1"
port = 8000
reload = True
reload_dirs = ["app"]  # Auto-reload when files in 'app' change
log_level = "info"
access_log = True

# For production, set these:
# reload = False
# workers = 4  # or (2 * cpu_count) + 1
