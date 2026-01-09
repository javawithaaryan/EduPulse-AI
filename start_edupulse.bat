@echo off
echo ===================================================
echo   Starting EduPulse AI Platform (Deployment Mode)
echo ===================================================
echo.

echo [1/3] Setting up environment...
set PYTHONPATH=%~dp0backend
cd /d "%~dp0backend"

echo [2/3] Activating Python Virtual Environment...
call "%~dp0.venv\Scripts\activate.bat"

echo [3/3] Launching Backend Server...
start "" "http://localhost:5000"
echo.
echo Application is running at http://localhost:5000
echo Press Ctrl+C to stop.
echo.
python app.py
pause
