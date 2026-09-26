@echo off
echo ========================================================
echo   Starting AXIOM Sentinel - Zero-Trust AI Invariant Suite
echo ========================================================
echo.

echo [1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "Axiom Backend API" cmd /k "cd /d %~dp0backend && python main.py"

echo [2/2] Starting Vite React Frontend on http://localhost:5173 ...
start "Axiom Frontend Dashboard" cmd /k "cd /d %~dp0frontend && npm.cmd run dev"

echo.
echo Both servers launched! Open http://localhost:5173 in your browser.
echo ========================================================
pause
