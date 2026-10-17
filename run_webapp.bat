@echo off
chcp 65001 >nul
title WEPAPP - Royal Thai Army Armament & Document Dashboard
echo ===============================================================================
echo  [WEPAPP] ROYAL THAI ARMY ARMAMENT & PRODUCTION DOCUMENT SYSTEM
echo ===============================================================================
echo.
echo Starting FastAPI Web Server at http://127.0.0.1:8000 ...
echo.

start "" "http://127.0.0.1:8000"

if exist "%~dp0.venv\Scripts\python.exe" (
    "%~dp0.venv\Scripts\python.exe" -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
) else if exist "C:\Users\EVE\miniconda3\python.exe" (
    "C:\Users\EVE\miniconda3\python.exe" -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
) else (
    python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
)

pause
