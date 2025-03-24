@echo off
echo Installing required Python packages...

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b
)

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo Installation complete!
pause
