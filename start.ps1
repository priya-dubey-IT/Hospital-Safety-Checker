# Hospital Safety Checker - Startup Script
# This script starts both backend and frontend servers

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Hospital Safety Checker - Starting..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if SQLite database exists
$dbPath = Join-Path $PSScriptRoot "backend\hospital_safety.db"
if (Test-Path $dbPath) {
    Write-Host "[OK] SQLite database found" -ForegroundColor Green
}
else {
    Write-Host "[!] SQLite database not found. It will be created on startup." -ForegroundColor Yellow
}

Write-Host ""

# Start Backend
Write-Host "Starting Backend Server..." -ForegroundColor Yellow
$backendPath = Join-Path $PSScriptRoot "backend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; .\venv\Scripts\Activate.ps1; python main.py" -WindowStyle Normal

Write-Host "[OK] Backend starting on http://localhost:8000" -ForegroundColor Green
Start-Sleep -Seconds 3

# Start Frontend
Write-Host "Starting Frontend Server..." -ForegroundColor Yellow
$frontendPath = Join-Path $PSScriptRoot "frontend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; npm run dev" -WindowStyle Normal

Write-Host "[OK] Frontend starting on http://localhost:3000" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Application Started!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "Frontend: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "Two new terminal windows have opened." -ForegroundColor Yellow
Write-Host "Keep them running while using the application." -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Enter to exit this window..." -ForegroundColor Gray
Read-Host
