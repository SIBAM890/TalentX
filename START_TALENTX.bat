@echo off
REM TalentX Quick Start - Single Click Launch
REM Double-click this file to start TalentX

setlocal enabledelayedexpansion

echo.
echo Starting TalentX Development Server...
echo.

cd /d "%~dp0"

REM Check if ports are already in use
netstat -ano | find ":8000" >nul
if !errorlevel! equ 0 (
    echo Found existing API server on port 8000
) else (
    echo Starting API backend on port 8000...
    start "TalentX API" cmd /k python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    timeout /t 5 /nobreak
)

netstat -ano | find ":5173" >nul
if !errorlevel! equ 0 (
    echo Found existing Frontend server on port 5173
) else (
    echo Starting React frontend on port 5173...
    cd frontend-react
    start "TalentX Frontend" cmd /k npm run dev
    cd ..
    timeout /t 5 /nobreak
)

echo.
echo Opening TalentX in browser...
timeout /t 3 /nobreak
start http://localhost:5173

echo.
echo =========================================
echo TalentX is ready at:
echo   http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo =========================================
echo.
echo Keep the terminal windows open while using TalentX
pause
