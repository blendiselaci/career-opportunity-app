@echo off
cd /d "%~dp0"
start "Career Opportunity Manager Server" cmd /k "python run.py"
timeout /t 2 >nul
start "" http://127.0.0.1:5000/
