@echo off
echo ============================================================
echo COMPLETE DATABASE RESET - Windows Batch Script
echo ============================================================
echo.
echo This script will:
echo 1. Find and kill the uvicorn process
echo 2. Delete app.db
echo 3. Create new database with correct schema
echo 4. Restart the server
echo.
pause

echo.
echo [1/4] Stopping uvicorn server...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *uvicorn*" 2>nul
timeout /t 2 /nobreak >nul

echo [2/4] Deleting old database...
if exist app.db (
    del /F app.db
    echo     ✓ app.db deleted
) else (
    echo     ✓ No app.db found
)

echo [3/4] Creating new database...
python reset_database.py

echo.
echo [4/4] Starting server...
echo.
echo Run this command to start the server:
echo     python -m uvicorn app.main:app --reload
echo.
echo ============================================================
echo DONE! Now start the server manually.
echo ============================================================
pause
