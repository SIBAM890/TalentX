@echo off
REM TalentX Start Script
REM Starts both the FastAPI backend and React frontend

echo.
echo ╔════════════════════════════════════════╗
echo ║      TalentX Development Server        ║
echo ║     Starting backend and frontend...    ║
echo ╚════════════════════════════════════════╝
echo.

cd /d "%~dp0"

REM Start FastAPI backend in a new terminal
echo [1/2] Starting FastAPI backend on port 8000...
start "TalentX API Server" cmd /k "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait for API to start
timeout /t 5 /nobreak

REM Start React frontend dev server in a new terminal
echo [2/2] Starting React frontend on port 5173...
cd frontend-react
start "TalentX Frontend Server" cmd /k "npm install && npm run dev"

REM Wait for frontend to start
timeout /t 8 /nobreak

REM Open browser
echo.
echo ✓ Servers started! Opening TalentX in your browser...
echo.
start http://localhost:5173

echo.
echo ════════════════════════════════════════════════
echo TalentX is now running:
echo - Frontend: http://localhost:5173
echo - API Docs: http://localhost:8000/docs
echo ════════════════════════════════════════════════
echo.
pause
