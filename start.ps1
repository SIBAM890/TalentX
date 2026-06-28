# TalentX Development Server Launcher
# Starts both FastAPI backend and React frontend

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "   TalentX Development Server" -ForegroundColor Cyan
Write-Host "   Starting backend and frontend..." -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

$projectRoot = $PSScriptRoot

# Check if Python is installed
$pythonVersion = python --version 2>&1
Write-Host "Python found: $pythonVersion" -ForegroundColor Green

# Check if Node.js is installed
$nodeVersion = node --version
Write-Host "Node.js found: $nodeVersion" -ForegroundColor Green

# Install Python dependencies
Write-Host ""
Write-Host "[1/4] Checking Python dependencies..." -ForegroundColor Yellow
if (Test-Path "$projectRoot\requirements.txt") {
    pip install -q -r "$projectRoot\requirements.txt" 2>&1 | Out-Null
    Write-Host "Python dependencies installed" -ForegroundColor Green
}

# Start FastAPI backend
Write-Host "[2/4] Starting FastAPI backend on port 8000..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "-m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload" -WorkingDirectory $projectRoot -NoNewWindow

# Wait for API to initialize
Write-Host "      Waiting for API to start..." -ForegroundColor Gray
Start-Sleep -Seconds 4

# Start React frontend
Write-Host ""
Write-Host "[3/4] Checking frontend dependencies..." -ForegroundColor Yellow
$frontendPath = "$projectRoot\frontend-react"
if (Test-Path "$frontendPath\package.json") {
    $nodeModulesPath = "$frontendPath\node_modules"
    if (-not (Test-Path $nodeModulesPath)) {
        Write-Host "      Installing npm packages..." -ForegroundColor Gray
        npm install --prefix $frontendPath --silent 2>&1 | Out-Null
    }
    Write-Host "Frontend dependencies ready" -ForegroundColor Green
}

Write-Host "[4/4] Starting React frontend on port 5173..." -ForegroundColor Yellow
Start-Process -FilePath "npm" -ArgumentList "run dev" -WorkingDirectory $frontendPath -NoNewWindow

# Wait for frontend to start
Start-Sleep -Seconds 5

# Open browser
Write-Host ""
Write-Host "Servers started! Opening TalentX in browser..." -ForegroundColor Green
Start-Sleep -Seconds 2
Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "TalentX is now running:" -ForegroundColor Cyan
Write-Host "  Frontend:  http://localhost:5173" -ForegroundColor Yellow
Write-Host "  API Docs:  http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
