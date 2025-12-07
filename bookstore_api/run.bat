@echo off
echo Starting Bookstore Management API...
echo.

REM Activate virtual environment if it exists
if exist "..\flask_env\Scripts\activate.bat" (
    call ..\flask_env\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found. Using system Python.
    echo.
)

REM Start the Flask application
python app.py
