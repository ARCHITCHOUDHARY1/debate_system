@echo off
echo ================================================
echo Debate System Setup
echo ================================================
echo.

REM Check if requirements.txt exists
if not exist requirements.txt (
    echo ERROR: requirements.txt not found
    echo Please ensure you are in the correct directory
    pause
    exit /b 1
)

echo [1/5] Initializing UV project...
uv init
if errorlevel 1 (
    echo ERROR: Failed to initialize UV project
    echo Please make sure UV is installed correctly
    pause
    exit /b 1
)

echo [2/5] Creating virtual environment...
uv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [3/5] Activating virtual environment...
call .venv\Scripts\activate
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [4/5] Installing dependencies from requirements.txt...
uv pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [5/5] Verifying installation...
python -c "import langgraph; import langchain_mistralai; print('All packages imported successfully')"
if errorlevel 1 (
    echo WARNING: Package verification failed
    echo Setup completed but some packages may not be installed correctly
)

echo.
echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo Next Steps:
echo 1. Verify your API key is set in .env file
echo 2. Run the debate system: python main.py
echo.
pause