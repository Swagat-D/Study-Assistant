@echo off
echo ===== Starting Study Assistant Backend =====

:: Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found. Please run install_windows.bat first.
    pause
    exit /b 1
)

:: Activate virtual environment
call venv\Scripts\activate

:: Start the server
echo Starting FastAPI server...
uvicorn app.main:app --reload

pause