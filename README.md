# AI Buddy

Lightweight FastAPI-based assistant framework for agents, LLMs and LMS integrations.

## Requirements

- Python 3.10+
- Install dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell (Windows)
pip install -r requirements.txt
```

## Run

Start the app with Uvicorn:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 and the OpenAPI docs at http://127.0.0.1:8000/docs

## Debugging in VS Code

A launch configuration is included at [.vscode/launch.json](.vscode/launch.json) to start the server under the debugger. Use Run → Start Debugging or select "Python: Uvicorn (FastAPI)".

## Project layout

- `app/` — FastAPI application and routes
- `core/` — agents, llm adapters, services
- `infrastructure/` — startup, db, cache, auth utilities
- `config/` — settings and logging
- `tests/` — tests

## Notes

- Ensure environment variables required by `app/config/settings.py` are set (see that file).
- For production use, run with a production ASGI server or behind a process manager.
