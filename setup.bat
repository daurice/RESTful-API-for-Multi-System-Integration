@echo off
echo ========================================
echo Bookstore Management API - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Python detected
python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist "flask_env" (
    echo [2/4] Creating virtual environment...
    python -m venv flask_env
    echo Virtual environment created successfully
) else (
    echo [2/4] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [3/4] Activating virtual environment...
call flask_env\Scripts\activate.bat
echo.

REM Install dependencies
echo [4/4] Installing dependencies...
cd bookstore_api
pip install -r requirements.txt
echo.

echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To start the API:
echo   1. cd bookstore_api
echo   2. python app.py
echo   OR simply run: bookstore_api\run.bat
echo.
echo API will be available at: http://localhost:5000
echo Documentation at: http://localhost:5000/api/docs
echo.
pause
