# Debate System Setup Script for PowerShell
# Usage: .\setup.ps1

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Debate System Setup" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if requirements.txt exists
if (-not (Test-Path "requirements.txt")) {
    Write-Host "ERROR: requirements.txt not found" -ForegroundColor Red
    Write-Host "Please ensure you are in the correct directory" -ForegroundColor Yellow
    exit 1
}

# Check if UV is installed
try {
    $uvVersion = uv --version 2>$null
    Write-Host "UV Version: $uvVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: UV is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Install UV from: https://github.com/astral-sh/uv" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "[1/5] Initializing UV project..." -ForegroundColor Yellow
try {
    uv init
    if ($LASTEXITCODE -ne 0) { throw "UV init failed" }
    Write-Host "SUCCESS: Project initialized" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to initialize UV project" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[2/5] Creating virtual environment..." -ForegroundColor Yellow
try {
    uv venv
    if ($LASTEXITCODE -ne 0) { throw "UV venv failed" }
    Write-Host "SUCCESS: Virtual environment created" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[3/5] Activating virtual environment..." -ForegroundColor Yellow
try {
    & .\.venv\Scripts\Activate.ps1
    Write-Host "SUCCESS: Virtual environment activated" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[4/5] Installing dependencies from requirements.txt..." -ForegroundColor Yellow
try {
    uv pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw "Package installation failed" }
    Write-Host "SUCCESS: All dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[5/5] Verifying installation..." -ForegroundColor Yellow
try {
    python -c "import langgraph; import langchain_mistralai; print('All packages imported successfully')"
    if ($LASTEXITCODE -ne 0) { throw "Import verification failed" }
    Write-Host "SUCCESS: Package verification passed" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Package verification failed" -ForegroundColor Yellow
    Write-Host "Setup completed but some packages may not be installed correctly" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Verify your API key is set in .env file"
Write-Host "2. Run the debate system: python main.py"
Write-Host ""
