@echo off
title Hospital Safety Checker - Launcher
cd /d "%~dp0"
echo Starting Hospital Safety Checker...
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0start.ps1"
if %errorlevel% neq 0 (
    echo.
    echo An error occurred while trying to run the startup script.
    pause
)
