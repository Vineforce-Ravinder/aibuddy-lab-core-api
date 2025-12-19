# PowerShell script to run Uvicorn with preset config
# Usage: .\run_uvicorn.ps1

$env:PYTHONPATH = $PSScriptRoot

Write-Host "Starting AI Buddy FastAPI server..." -ForegroundColor Green
Write-Host "Host: 127.0.0.1, Port: 8000, Reload: enabled" -ForegroundColor Cyan

& uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
