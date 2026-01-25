@echo off
echo Starting EduPulse AI...

REM Backend
start cmd /k "
cd /d %~dp0
call .venv\Scripts\activate
cd backend
flask run
"

REM Frontend
start cmd /k "
cd /d %~dp0
cd Frontend
npm run dev
"

echo EduPulse AI is starting...
