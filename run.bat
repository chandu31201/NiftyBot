@echo off
title NiftyBot Launcher
color 0A

echo.
echo  ==========================================
echo   NIFTYBOT - Starting up...
echo  ==========================================
echo.

:: ── Check Python ──
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found!
    echo  Go to python.org and install Python first.
    echo  Make sure to tick "Add Python to PATH"
    pause
    exit /b
)

:: ── Check Node ──
node --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Node.js not found!
    echo  Go to nodejs.org and install Node.js first.
    pause
    exit /b
)

:: ── Install backend dependencies ──
echo  [1/4] Installing backend dependencies...
cd backend
pip install -r requirements.txt --quiet
cd ..

:: ── Install frontend dependencies ──
echo  [2/4] Installing frontend dependencies...
cd frontend
call npm install --silent
cd ..

:: ── Start FastAPI backend ──
echo  [3/4] Starting FastAPI backend on port 8000...
start "NiftyBot Backend" cmd /k "cd backend && python -m uvicorn main:app --reload --port 8000"

:: ── Wait for backend to be ready ──
timeout /t 4 /nobreak >nul

:: ── Start Angular frontend ──
echo  [4/4] Starting Angular frontend...
start "NiftyBot Frontend" cmd /k "cd frontend && npm start"

:: ── Wait then open browser ──
timeout /t 8 /nobreak >nul
start http://localhost:4200

echo.
echo  ==========================================
echo   NiftyBot is running!
echo   Dashboard: http://localhost:4200
echo   API Docs:  http://localhost:8000/docs
echo  ==========================================
echo.
echo  Close both black windows to stop the bot.
pause
